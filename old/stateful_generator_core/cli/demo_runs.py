import os
import sys
import tempfile

ROOT = "/Users/chris/code/gemini"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from stateful_generator_core.core.config import EngineConfig
from stateful_generator_core.core.graph_store import GraphStore
from stateful_generator_core.core.idea_engine import IdeaEngine


CONFIGS = [
    "museum_engine.json",
    "trump_engine.json",
    "data_research_engine.json",
    "georgia_mining_engine.json",
]


def run_demo():
    base_dir = "/Users/chris/code/gemini/stateful_generator_core/configs"
    with tempfile.TemporaryDirectory() as tmpdir:
        for config_name in CONFIGS:
            config_path = os.path.join(base_dir, config_name)
            config = EngineConfig.load(config_path)
            store = GraphStore(os.path.join(tmpdir, config_name.replace(".json", "")))
            engine = IdeaEngine(config, store, seed=7)
            first_agent = config.agents[0]["id"]
            result = engine.run(agent_id=first_agent)
            print(f"[{config.name}] Agent {result.agent_id} created {len(result.created_nodes)} node(s) and {len(result.created_edges)} edge(s).")


if __name__ == "__main__":
    run_demo()
