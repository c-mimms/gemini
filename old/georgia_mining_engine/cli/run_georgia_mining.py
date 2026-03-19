import argparse
import os
import subprocess
import sys

ROOT = "/Users/chris/code/gemini"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from georgia_mining_engine.core.georgia_mining_pipeline import GeorgiaMiningPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Georgia Mining research engine.")
    parser.add_argument("--base-dir", default="/Users/chris/code/gemini/georgia_mining_engine")
    parser.add_argument("--config", default="/Users/chris/code/gemini/georgia_mining_engine/configs/georgia_mining_engine.json")
    parser.add_argument("--data-dir", default="/Users/chris/code/gemini/georgia_mining_engine/data")
    parser.add_argument("--offline", action="store_true", help="Disable web research and use stub model.")
    parser.add_argument("--publish", action="store_true", help="Publish the mining site after generation.")
    args = parser.parse_args()

    pipeline = GeorgiaMiningPipeline(
        base_dir=args.base_dir,
        config_path=args.config,
        data_dir=args.data_dir,
        offline=args.offline,
        seed=7,
    )
    result = pipeline.run()

    print(f"Generated: {result.article_path}")
    print(f"Format: {result.format_name}")
    print(f"Topic: {result.topic}")

    if args.publish:
        cmd = [
            "python3",
            "/Users/chris/code/gemini/static_site/build_georgia_mining.py",
            "--source",
            os.path.join(args.base_dir, "articles"),
            "--s3-bucket",
            "s3://gemini-designs-portfolio-2026-v2/georgia-mining/",
            "--data-dir",
            args.data_dir,
        ]
        subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
