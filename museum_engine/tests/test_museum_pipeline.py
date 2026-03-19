import os
import tempfile
import unittest

from stateful_generator_core.core.config import EngineConfig
from stateful_generator_core.core.storage_wrapper import StorageWrapper
from stateful_generator_core.core.run_log import RunLogger
from stateful_generator_core.core.tool_registry import ToolRegistry
from museum_engine.core.model import load_model
from museum_engine.core.llm_idea_engine import LLMIdeaEngine


class MuseumPipelineTests(unittest.TestCase):
    def test_offline_run_creates_article_using_llm_engine(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = os.path.join(tmpdir, "museum_engine")
            os.makedirs(base_dir, exist_ok=True)
            os.makedirs(os.path.join(base_dir, "articles"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, "prompts"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, "configs"), exist_ok=True)

            prompt_src = "/Users/chris/code/gemini/museum_engine/prompts/museum_task.md"
            config_src = "/Users/chris/code/gemini/museum_engine/configs/museum_engine.json"
            with open(prompt_src, "r", encoding="utf-8") as f:
                prompt_text = f.read()
            with open(os.path.join(base_dir, "prompts", "museum_task.md"), "w", encoding="utf-8") as f:
                f.write(prompt_text)
            with open(config_src, "r", encoding="utf-8") as f:
                config_text = f.read()
            with open(os.path.join(base_dir, "configs", "museum_engine.json"), "w", encoding="utf-8") as f:
                f.write(config_text)

            config = EngineConfig.load(os.path.join(base_dir, "configs", "museum_engine.json"))
            storage = StorageWrapper(os.path.join(base_dir, "state"))
            logger = RunLogger(os.path.join(base_dir, "state"))
            model = load_model()
            registry = ToolRegistry()

            engine = LLMIdeaEngine(
                config=config,
                storage=storage,
                run_logger=logger,
                tool_registry=registry,
                model=model,
                seed=1,
            )

            article_node = None
            # Run simulation
            for _ in range(30):
                try:
                    result = engine.run()
                    for node in result.created_nodes:
                        if node.type == "Article":
                            article_node = node
                            break
                    if article_node:
                        break
                except Exception as e:
                    # Ignore validation errors for agents called too early
                    pass

            self.assertIsNotNone(article_node, "Engine failed to output an Article node.")
            self.assertIn("<main class=\"museum-body\">", article_node.content)
            self.assertIn("<div class=\"metadata\"", article_node.content)

            # Check run log
            runs_dir = os.path.join(base_dir, "state", "runs")
            run_files = os.listdir(runs_dir)
            self.assertTrue(len(run_files) > 0)


if __name__ == "__main__":
    unittest.main()
