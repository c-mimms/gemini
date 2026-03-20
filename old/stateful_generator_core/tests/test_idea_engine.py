import json
import os
import tempfile
import unittest

from stateful_generator_core.core.config import EngineConfig
from stateful_generator_core.core.graph_store import GraphStore
from stateful_generator_core.core.idea_engine import IdeaEngine, ValidationError
from stateful_generator_core.core.run_log import RunLogger
from stateful_generator_core.core.storage_wrapper import StorageWrapper
from stateful_generator_core.core.tool_registry import ToolRegistry


BASE_DIR = "/Users/chris/code/gemini/stateful_generator_core"


class IdeaEngineTests(unittest.TestCase):
    def test_run_creates_nodes_and_edges(self):
        config_path = os.path.join(BASE_DIR, "configs", "museum_engine.json")
        config = EngineConfig.load(config_path)
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = StorageWrapper(tmpdir)
            store = storage._store
            # Seed required inputs for the writer
            fact = store.create_node("Fact", "Seed fact", "seed_agent")
            outline = store.create_node("Outline", "Seed outline", "seed_agent")

            engine = IdeaEngine(config, storage, seed=123)
            result = engine.run(agent_id="museum_writer")

            self.assertEqual(result.agent_id, "museum_writer")
            self.assertEqual(len(result.created_nodes), 1)
            self.assertEqual(result.created_nodes[0].type, "Article")
            self.assertGreaterEqual(len(result.created_edges), 2)
            # Ensure cite edges were created
            cite_edges = [e for e in result.created_edges if e.type == "cites"]
            self.assertGreaterEqual(len(cite_edges), 1)
            # Ensure derived_from edges link to inputs
            targets = {e.to_id for e in result.created_edges}
            self.assertIn(fact.id, targets)
            self.assertIn(outline.id, targets)

    def test_format_validator_rejects_missing_fragment(self):
        custom_config = {
            "name": "Format Test Engine",
            "version": 1,
            "node_types": {"Article": {"description": "Article", "immutable_content": True}},
            "edge_types": {"derived_from": {"description": "Derived"}},
            "agents": [
                {
                    "id": "writer",
                    "role": "Writer",
                    "permissions": {"web_search": False, "read_types": [], "write_types": ["Article"]},
                    "input_policy": {"max_nodes": 0},
                    "output_policy": {
                        "outputs": [{"type": "Article", "content_template": "<main>Missing class</main>"}],
                        "link_to_inputs": None,
                        "cite_inputs": False
                    }
                }
            ],
            "validators": {
                "schema": True,
                "format": {"Article": {"must_include": ["class=\"article-body\""]}}
            },
            "run_policy": {"agent_weights": {"writer": 1}, "max_outputs_per_run": 1}
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(custom_config, f)
            config = EngineConfig.load(config_path)
            storage = StorageWrapper(tmpdir)
            engine = IdeaEngine(config, storage)
            with self.assertRaises(ValidationError):
                engine.run(agent_id="writer")

    def test_engine_writes_run_log(self):
        config_path = os.path.join(BASE_DIR, "configs", "museum_engine.json")
        config = EngineConfig.load(config_path)
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = StorageWrapper(tmpdir)
            run_logger = RunLogger(tmpdir)
            tool_registry = ToolRegistry()
            engine = IdeaEngine(config, storage, run_logger=run_logger, tool_registry=tool_registry, seed=123)
            
            store = storage._store
            store.create_node("Fact", "Seed fact", "seed_agent")
            store.create_node("Outline", "Seed outline", "seed_agent")
            
            result = engine.run(agent_id="museum_writer")
            
            runs_dir = os.path.join(tmpdir, "runs")
            run_files = os.listdir(runs_dir)
            self.assertEqual(len(run_files), 1)
            
            run_id = run_files[0].replace(".json", "")
            record = run_logger.load_run(run_id)
            self.assertEqual(record["status"], "success")
            self.assertEqual(record["agent_id"], "museum_writer")
            self.assertEqual(record["config_snapshot"]["name"], config.name)
            self.assertIn(result.created_nodes[0].id, record["outputs"])

    def test_metadata_update_preserves_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(tmpdir)
            node = store.create_node("Idea", "Immutable content", "seed_agent")
            store.update_metadata(node.id, {"status": "approved"})
            refreshed = store.nodes[node.id]
            self.assertEqual(refreshed.content, "Immutable content")
            self.assertEqual(refreshed.metadata.get("status"), "approved")


if __name__ == "__main__":
    unittest.main()
