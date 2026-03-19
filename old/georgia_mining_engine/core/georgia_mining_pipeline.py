import csv
import json
import os
import random
import re
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional

from .config import EngineConfig
from .graph_store import GraphStore
from .model import load_model
from .web_research import maybe_search, maybe_fetch
from stateful_generator_core.core.run_log import RunLogger


FORMATS = ["A", "B", "C"]


@dataclass
class PipelineResult:
    article_path: str
    format_name: str
    topic: str


class GeorgiaMiningPipeline:
    def __init__(self, base_dir: str, config_path: str, data_dir: str, offline: bool = False, seed: Optional[int] = None):
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.offline = offline
        self.random = random.Random(seed)
        self.config = EngineConfig.load(config_path)
        self.store = GraphStore(os.path.join(base_dir, "state"))
        self.run_logger = RunLogger(os.path.join(base_dir, "state"))
        self.model = load_model()

    def run(self) -> PipelineResult:
        run_record = self.run_logger.start_run(agent_id="georgia_mining_pipeline", config_snapshot=getattr(self.config, "raw", {}))
        
        datasets = self._list_datasets()
        format_name = self._select_format()
        topic = self._select_topic(format_name, datasets)
        profiles = self._profile_datasets(datasets)
        facts = self._derive_facts(profiles)
        narrative = self._narrative(topic, format_name, facts)
        article_html = self._render_article(topic, format_name, profiles, facts, narrative)
        article_path = self._save_article(article_html, topic)
        self._record_nodes(format_name, topic, datasets, profiles, facts, narrative, article_html, article_path)
        
        record = self.run_logger.load_run(run_record.run_id)
        record["format_name"] = format_name
        self.run_logger._write(run_record.run_id, record)
        
        self.run_logger.finish_run(run_record, status="success", outputs=[])
        return PipelineResult(article_path=article_path, format_name=format_name, topic=topic)

    def _list_datasets(self) -> List[str]:
        if not os.path.exists(self.data_dir):
            return []
        files = []
        for name in os.listdir(self.data_dir):
            path = os.path.join(self.data_dir, name)
            if os.path.isfile(path):
                if name.lower() == "manifest.md":
                    continue
                ext = os.path.splitext(name)[1].lower()
                if ext in [".csv", ".tsv", ".xlsx", ".pdf", ".zip", ".geojson", ".rdb"]:
                    files.append(name)
        return sorted(files)

    def _select_format(self) -> str:
        history_path = os.path.join(self.base_dir, "state", "format_history.json")
        counts: Dict[str, int] = {fmt: 0 for fmt in FORMATS}
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                counts.update(json.load(f))
        min_count = min(counts.values())
        candidates = [fmt for fmt, count in counts.items() if count == min_count]
        choice = self.random.choice(candidates)
        counts[choice] += 1
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(counts, f, indent=2)
        return choice

    def _select_topic(self, format_name: str, datasets: List[str]) -> str:
        if format_name == "B":
            return "Georgia Mining Dataset Catalog"
        if datasets:
            return f"Data analysis of {datasets[0]}"
        return "Georgia Mining Data Overview"

    def _profile_datasets(self, datasets: List[str]) -> List[Dict[str, str]]:
        profiles = []
        for name in datasets[:8]:
            path = os.path.join(self.data_dir, name)
            profile = {
                "file": name,
                "size_bytes": str(os.path.getsize(path)),
                "rows": "unknown",
                "columns": "unknown",
                "numeric_summary": "",
            }
            ext = os.path.splitext(name)[1].lower()
            if ext in [".csv", ".tsv"]:
                delimiter = "\t" if ext == ".tsv" else ","
                rows, cols, numeric_summary = self._profile_tabular(path, delimiter)
                profile["rows"] = str(rows)
                profile["columns"] = str(cols)
                profile["numeric_summary"] = numeric_summary
            profiles.append(profile)
        return profiles

    def _profile_tabular(self, path: str, delimiter: str) -> (int, int, str):
        rows = 0
        numeric_stats: Dict[str, Dict[str, float]] = {}
        headers: List[str] = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f, delimiter=delimiter)
            for i, row in enumerate(reader):
                if i == 0:
                    headers = row
                    continue
                rows += 1
                for idx, value in enumerate(row[: len(headers)]):
                    try:
                        num = float(value)
                    except Exception:
                        continue
                    key = headers[idx] if idx < len(headers) else f"col_{idx}"
                    stats = numeric_stats.setdefault(key, {"min": num, "max": num, "sum": 0.0, "count": 0.0})
                    stats["min"] = min(stats["min"], num)
                    stats["max"] = max(stats["max"], num)
                    stats["sum"] += num
                    stats["count"] += 1
                if rows >= 5000:
                    break
        cols = len(headers)
        summaries = []
        for key, stats in list(numeric_stats.items())[:3]:
            avg = stats["sum"] / stats["count"] if stats["count"] else 0.0
            summaries.append(f"{key}: min {stats['min']:.2f}, max {stats['max']:.2f}, mean {avg:.2f}")
        return rows, cols, "; ".join(summaries)

    def _derive_facts(self, profiles: List[Dict[str, str]]) -> List[str]:
        facts = []
        for profile in profiles:
            facts.append(
                f"{profile['file']} has approximately {profile['rows']} rows and {profile['columns']} columns."
            )
            if profile["numeric_summary"]:
                facts.append(f"{profile['file']} numeric summary: {profile['numeric_summary']}.")
        if self.offline:
            return facts
        if facts:
            return facts
        return ["No dataset facts available."]

    def _narrative(self, topic: str, format_name: str, facts: List[str]) -> str:
        if self.offline:
            return f"Research narrative for {topic} ({format_name})."
        system_prompt = "Write a concise research narrative grounded in the provided facts."
        user_prompt = f"Topic: {topic}\nFormat: {format_name}\nFacts:\n- " + "\n- ".join(facts)
        return self.model.generate(system_prompt=system_prompt, user_prompt=user_prompt).text

    def _render_article(self, topic: str, format_name: str, profiles: List[Dict[str, str]], facts: List[str], narrative: str) -> str:
        datasets_meta = ", ".join([p["file"] for p in profiles])
        html = [
            "<main class=\"geo-body\">",
            "<div class=\"metadata\" style=\"display:none;\">",
            f"<meta name=\"title\" content=\"{topic}\">",
            f"<meta name=\"description\" content=\"Research-focused mining analysis.\">",
            f"<meta name=\"tag\" content=\"Format {format_name} | Research\">",
            f"<meta name=\"datasets\" content=\"{datasets_meta}\">",
            "</div>",
            f"<h1>{topic}</h1>",
            "<div class=\"key-findings\">",
            "<h2>Key Findings</h2>",
        ]
        for fact in facts[:5]:
            html.append(f"<p>{fact}</p>")
        html.append("</div>")

        html.append("<div class=\"data-table-wrapper\"><table class=\"data-table\">")
        html.append("<thead><tr><th>Dataset</th><th>Rows</th><th>Columns</th><th>Notes</th></tr></thead>")
        html.append("<tbody>")
        for profile in profiles:
            html.append(
                f"<tr><td>{profile['file']}</td><td>{profile['rows']}</td><td>{profile['columns']}</td><td>{profile['numeric_summary']}</td></tr>"
            )
        html.append("</tbody></table></div>")

        html.append("<div class=\"stat-grid\">")
        for profile in profiles[:2]:
            html.append(
                "<div class=\"stat-callout\">"
                f"<div class=\"stat-number\">{profile['rows']}</div>"
                f"<div class=\"stat-label\">Rows in {profile['file']}</div>"
                "</div>"
            )
        html.append("</div>")

        html.append("<h2>Research Narrative</h2>")
        html.append(f"<p>{narrative}</p>")
        html.append("</main>")
        return "".join(html)

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
        datasets: List[str],
        profiles: List[Dict[str, str]],
        facts: List[str],
        narrative: str,
        article_html: str,
        article_path: str,
    ) -> None:
        topic_node = self.store.create_node("ResearchQuestion", topic, "question_selector")

        dataset_nodes = []
        for name in datasets:
            node = self.store.create_node("Dataset", name, "dataset_loader")
            self.store.create_edge(node.id, topic_node.id, "derived_from")
            dataset_nodes.append(node)

        profile_nodes = []
        for profile in profiles:
            node = self.store.create_node("Profile", json.dumps(profile), "profiler")
            for dataset in dataset_nodes:
                if dataset.content == profile["file"]:
                    self.store.create_edge(node.id, dataset.id, "cites")
            profile_nodes.append(node)

        fact_nodes = []
        for fact in facts:
            node = self.store.create_node("Fact", fact, "fact_builder")
            for profile in profile_nodes:
                self.store.create_edge(node.id, profile.id, "derived_from")
            fact_nodes.append(node)

        synthesis_node = self.store.create_node("Synthesis", narrative, "synthesizer")
        for fact in fact_nodes:
            self.store.create_edge(synthesis_node.id, fact.id, "derived_from")

        article_node = self.store.create_node("Article", article_html, "writer", {"path": article_path, "format": format_name})
        self.store.create_edge(article_node.id, synthesis_node.id, "derived_from")
        for dataset in dataset_nodes:
            self.store.create_edge(article_node.id, dataset.id, "cites")

    def _slugify(self, text: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
        return slug[:80] if slug else "georgia-mining-article"
