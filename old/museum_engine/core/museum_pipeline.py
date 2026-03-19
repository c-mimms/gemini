import json
import os
import random
import re
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Tuple

from .config import EngineConfig
from .graph_store import GraphStore
from .model import load_model
from .image_tools import download_image
from .web_research import maybe_fetch, maybe_search
from stateful_generator_core.core.run_log import RunLogger


FORMATS = [
    "Deep Dive",
    "Placard",
    "Biography",
    "Spotlight",
    "Thematic Path",
    "Audio Script",
    "Lesson Plan",
    "Scavenger Hunt",
    "Discussion Guide",
]

FALLBACK_TOPICS = [
    "The Jacquard Loom and Programmable Weaving",
    "Seymour Cray and the Rise of Supercomputing",
    "The Xerox Alto and the GUI Revolution",
    "The Apollo Guidance Computer and Rope Memory",
    "The Osborne 1 and Portable Computing",
    "The Commodore 64 and Home Computing",
]


@dataclass
class PipelineResult:
    article_path: str
    format_name: str
    topic: str


class MuseumPipeline:
    def __init__(self, base_dir: str, config_path: str, offline: bool = False, seed: Optional[int] = None):
        self.base_dir = base_dir
        self.offline = offline
        self.random = random.Random(seed)
        self.config = EngineConfig.load(config_path)
        self.store = GraphStore(os.path.join(base_dir, "state"))
        self.run_logger = RunLogger(os.path.join(base_dir, "state"))
        self.model = load_model()

    def run(self) -> PipelineResult:
        run_record = self.run_logger.start_run(agent_id="museum_pipeline", config_snapshot=getattr(self.config, "raw", {}))
        
        existing_topics = self._existing_topics()
        format_name = self._select_format()
        topic = self._select_topic(format_name, existing_topics)
        sources, facts = self._research(topic)
        images = self._select_images(topic)
        outline = self._outline(topic, format_name, facts)
        article_html = self._write_article(topic, format_name, facts, outline, images)
        article_path = self._save_article(article_html, topic)
        self._record_nodes(format_name, topic, sources, facts, outline, article_html, article_path)
        
        record = self.run_logger.load_run(run_record.run_id)
        record["format_name"] = format_name
        self.run_logger._write(run_record.run_id, record)
        
        self.run_logger.finish_run(run_record, status="success", outputs=[])
        return PipelineResult(article_path=article_path, format_name=format_name, topic=topic)

    def _existing_topics(self) -> List[str]:
        articles_dir = os.path.join(self.base_dir, "articles")
        if not os.path.exists(articles_dir):
            return []
        topics = []
        for name in os.listdir(articles_dir):
            if name.endswith(".html"):
                slug = name.split("_", 1)[-1].replace(".html", "")
                topics.append(slug.replace("-", " "))
        return topics

    def _select_format(self) -> str:
        history_path = os.path.join(self.base_dir, "state", "format_history.json")
        counts: Dict[str, int] = {fmt: 0 for fmt in FORMATS}
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            counts.update(loaded)
        min_count = min(counts.values())
        candidates = [fmt for fmt, count in counts.items() if count == min_count]
        choice = self.random.choice(candidates)
        counts[choice] += 1
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(counts, f, indent=2)
        return choice

    def _select_topic(self, format_name: str, existing_topics: List[str]) -> str:
        if self.offline:
            for topic in FALLBACK_TOPICS:
                if topic.lower() not in " ".join(existing_topics).lower():
                    return topic
            return FALLBACK_TOPICS[0]

        system_prompt = "You are a museum curator selecting a new, non-duplicative topic."
        user_prompt = (
            f"Select a topic for format {format_name}. Avoid duplicates.\n"
            f"Existing topics (slugs): {existing_topics}\n"
            "Return a single topic string."
        )
        response = self.model.generate(system_prompt=system_prompt, user_prompt=user_prompt).text
        topic = response.strip().splitlines()[0]
        return topic

    def _research(self, topic: str) -> Tuple[List[Dict[str, str]], List[str]]:
        sources = []
        facts = []
        results = maybe_search(topic, max_results=5, offline=self.offline)
        for result in results:
            page = maybe_fetch(result.url, offline=self.offline)
            if not page:
                continue
            sources.append({"title": page.title, "url": page.url})
            snippet = page.text[:400]
            if snippet:
                facts.append(f"{page.title}: {snippet}")
        if self.offline:
            sources.append({"title": "Offline Reference", "url": "offline://reference"})
            facts.append(f"Offline fact seed for {topic}.")
        return sources, facts

    def _select_images(self, topic: str) -> List[str]:
        if self.offline:
            return []
        system_prompt = "Return a JSON array of Wikimedia Commons filenames relevant to the topic."
        user_prompt = f"Topic: {topic}\nReturn only a JSON array of filenames."
        response = self.model.generate(system_prompt=system_prompt, user_prompt=user_prompt).text
        try:
            filenames = json.loads(response)
        except Exception:
            return []
        if not isinstance(filenames, list):
            return []
        downloaded = []
        for filename in filenames[:3]:
            if not isinstance(filename, str):
                continue
            url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}?width=1000"
            output_path = os.path.join(self.base_dir, "images", self._slugify(filename) + ".jpg")
            if download_image(url, output_path):
                downloaded.append(output_path)
        return downloaded

    def _outline(self, topic: str, format_name: str, facts: List[str]) -> str:
        if self.offline:
            return f"Outline for {topic} ({format_name})."
        system_prompt = "Create a concise outline for the museum piece using the provided facts."
        user_prompt = f"Topic: {topic}\nFormat: {format_name}\nFacts:\n- " + "\n- ".join(facts)
        return self.model.generate(system_prompt=system_prompt, user_prompt=user_prompt).text

    def _write_article(self, topic: str, format_name: str, facts: List[str], outline: str, images: List[str]) -> str:
        system_prompt = self._load_prompt()
        user_prompt = (
            f"Topic: {topic}\n"
            f"Format: {format_name}\n"
            f"Outline:\n{outline}\n"
            f"Facts:\n- " + "\n- ".join(facts) + "\n"
            f"Local Images:\n- " + "\n- ".join(images) + "\n"
            "Generate HTML now."
        )
        return self.model.generate(system_prompt=system_prompt, user_prompt=user_prompt).text

    def _save_article(self, html: str, topic: str) -> str:
        articles_dir = os.path.join(self.base_dir, "articles")
        os.makedirs(articles_dir, exist_ok=True)
        slug = self._slugify(topic)
        filename = f"{date.today().isoformat()}_{slug}.html"
        path = os.path.join(articles_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path

    def _record_nodes(
        self,
        format_name: str,
        topic: str,
        sources: List[Dict[str, str]],
        facts: List[str],
        outline: str,
        article_html: str,
        article_path: str,
    ) -> None:
        topic_node = self.store.create_node("Topic", topic, "museum_topic_selector")

        source_nodes = []
        for source in sources:
            node = self.store.create_node("Source", json.dumps(source), "museum_researcher")
            self.store.create_edge(node.id, topic_node.id, "derived_from")
            source_nodes.append(node)

        fact_nodes = []
        for fact in facts:
            node = self.store.create_node("Fact", fact, "museum_researcher")
            self.store.create_edge(node.id, topic_node.id, "derived_from")
            for source in source_nodes:
                self.store.create_edge(node.id, source.id, "cites")
            fact_nodes.append(node)

        outline_node = self.store.create_node("Outline", outline, "museum_outliner")
        for fact in fact_nodes:
            self.store.create_edge(outline_node.id, fact.id, "derived_from")

        article_node = self.store.create_node("Article", article_html, "museum_writer", {"path": article_path, "format": format_name})
        self.store.create_edge(article_node.id, outline_node.id, "derived_from")
        for fact in fact_nodes:
            self.store.create_edge(article_node.id, fact.id, "cites")

    def _slugify(self, text: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
        return slug[:80] if slug else "museum-article"

    def _load_prompt(self) -> str:
        prompt_path = os.path.join(self.base_dir, "prompts", "museum_task.md")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
