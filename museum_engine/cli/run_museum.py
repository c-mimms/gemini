import argparse
import os
import subprocess
import sys

ROOT = "/Users/chris/code/gemini"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from museum_engine.core.museum_pipeline import MuseumPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Mimms Museum engine.")
    parser.add_argument("--base-dir", default="/Users/chris/code/gemini/museum_engine")
    parser.add_argument("--config", default="/Users/chris/code/gemini/museum_engine/configs/museum_engine.json")
    parser.add_argument("--offline", action="store_true", help="Disable web research and use stub sources.")
    parser.add_argument("--publish", action="store_true", help="Publish the museum site after generation.")
    args = parser.parse_args()

    pipeline = MuseumPipeline(base_dir=args.base_dir, config_path=args.config, offline=args.offline, seed=7)
    result = pipeline.run()

    print(f"Generated: {result.article_path}")
    print(f"Format: {result.format_name}")
    print(f"Topic: {result.topic}")

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
