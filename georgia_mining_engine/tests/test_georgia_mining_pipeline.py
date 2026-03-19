import os
import tempfile
import unittest

from georgia_mining_engine.core.georgia_mining_pipeline import GeorgiaMiningPipeline


class GeorgiaMiningPipelineTests(unittest.TestCase):
    def test_offline_run_creates_article(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = os.path.join(tmpdir, "georgia_mining_engine")
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(base_dir, exist_ok=True)
            os.makedirs(os.path.join(base_dir, "articles"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, "prompts"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, "configs"), exist_ok=True)
            os.makedirs(data_dir, exist_ok=True)

            # Seed a small dataset
            csv_path = os.path.join(data_dir, "sample.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("site,production\nAlpha,10\nBeta,25\n")

            prompt_src = "/Users/chris/code/gemini/georgia_mining_engine/prompts/georgia_mining_task.md"
            config_src = "/Users/chris/code/gemini/georgia_mining_engine/configs/georgia_mining_engine.json"
            with open(prompt_src, "r", encoding="utf-8") as f:
                prompt_text = f.read()
            with open(os.path.join(base_dir, "prompts", "georgia_mining_task.md"), "w", encoding="utf-8") as f:
                f.write(prompt_text)
            with open(config_src, "r", encoding="utf-8") as f:
                config_text = f.read()
            with open(os.path.join(base_dir, "configs", "georgia_mining_engine.json"), "w", encoding="utf-8") as f:
                f.write(config_text)

            pipeline = GeorgiaMiningPipeline(
                base_dir=base_dir,
                config_path=os.path.join(base_dir, "configs", "georgia_mining_engine.json"),
                data_dir=data_dir,
                offline=True,
                seed=1,
            )
            result = pipeline.run()

            self.assertTrue(os.path.exists(result.article_path))
            with open(result.article_path, "r", encoding="utf-8") as f:
                html = f.read()
            self.assertIn("<main class=\"geo-body\">", html)
            self.assertIn("<meta name=\"datasets\"", html)


if __name__ == "__main__":
    unittest.main()
