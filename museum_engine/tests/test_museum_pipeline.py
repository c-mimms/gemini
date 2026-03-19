import os
import tempfile
import unittest

from museum_engine.core.museum_pipeline import MuseumPipeline


class MuseumPipelineTests(unittest.TestCase):
    def test_offline_run_creates_article(self):
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

            pipeline = MuseumPipeline(
                base_dir=base_dir,
                config_path=os.path.join(base_dir, "configs", "museum_engine.json"),
                offline=True,
                seed=1,
            )
            result = pipeline.run()

            self.assertTrue(os.path.exists(result.article_path))
            with open(result.article_path, "r", encoding="utf-8") as f:
                html = f.read()
            self.assertIn("<main class=\"museum-body\">", html)
            self.assertIn("<div class=\"metadata\"", html)


if __name__ == "__main__":
    unittest.main()
