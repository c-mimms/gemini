import argparse
import os
import subprocess
import sys
import re
import datetime

ROOT = "/Users/chris/code/gemini"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from stateful_generator_core.core.config import EngineConfig
from stateful_generator_core.core.storage_wrapper import StorageWrapper
from stateful_generator_core.core.run_log import RunLogger
from stateful_generator_core.core.tool_registry import ToolRegistry
from museum_engine.core.model import load_model
from museum_engine.core.llm_idea_engine import LLMIdeaEngine
from museum_engine.core.web_research import maybe_search


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Agentic Museum Engine.")
    parser.add_argument("--base-dir", default="/Users/chris/code/gemini/museum_engine")
    parser.add_argument("--config", default="/Users/chris/code/gemini/museum_engine/configs/museum_engine.json")
    parser.add_argument("--offline", action="store_true", help="Disable web research and use stub sources.")
    parser.add_argument("--publish", action="store_true", help="Publish the museum site after generation.")
    args = parser.parse_args()

    os.makedirs(os.path.join(args.base_dir, "state"), exist_ok=True)

    config = EngineConfig.load(args.config)
    storage = StorageWrapper(os.path.join(args.base_dir, "state"))
    logger = RunLogger(os.path.join(args.base_dir, "state"))
    model = load_model()

    registry = ToolRegistry()
    def web_search(query):
        if args.offline:
            return [{"url": "offline://reference", "title": "Offline Ref", "text": f"Offline seed for {query}."}]
        results = maybe_search(query, max_results=3, offline=args.offline)
        return [{"url": r.url, "title": r.title, "text": r.text} for r in results]
    
    registry.register("web_search", web_search)

    engine = LLMIdeaEngine(
        config=config,
        storage=storage,
        run_logger=logger,
        tool_registry=registry,
        model=model,
        seed=7
    )

    print("Starting agentic simulation...")
    
    max_steps = 50
    article_path = None
    topic = "Unknown Topic"
    
    for step in range(max_steps):
        try:
            result = engine.run()
            print(f"Step {step+1}: Agent {result.agent_id} generated {len(result.created_nodes)} nodes")
        except Exception as e:
            print(f"Step {step+1}: Agent run failed (likely missing prerequisites)")
            continue
            
        for node in result.created_nodes:
            if node.type == "Article":
                print(f"SUCCESS: Article node created!")
                
                os.makedirs(os.path.join(args.base_dir, "articles"), exist_ok=True)
                topic_nodes = storage._store.list_nodes(["Topic"])
                if topic_nodes:
                    topic = topic_nodes[0].content
                    slug = re.sub(r"[^a-zA-Z0-9]+", "-", topic.lower()).strip("-")
                else:
                    slug = "museum-article"
                    
                article_path = os.path.join(args.base_dir, "articles", f"{datetime.date.today().isoformat()}_{slug[:80]}.html")
                with open(article_path, "w", encoding="utf-8") as f:
                    f.write(node.content)
                break
        
        if article_path:
            break
            
    if not article_path:
        print("Failed to converge on an article.")
        sys.exit(1)

    print(f"Generated: {article_path}")

    if args.publish:
        cmd = [
            "python3",
            "/Users/chris/code/gemini/static_site/build_museum.py",
            "--source",
            os.path.join(args.base_dir, "articles"),
            "--s3-bucket",
            "s3://gemini-designs-portfolio-2026-v2/museum/",
            "--site-name",
            "Mimms Museum",
            "--site-tagline",
            "Preserving the artifacts of computing history",
        ]
        subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
