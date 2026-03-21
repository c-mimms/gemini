import json
import re
import os

db_path = "/Users/chris/code/gemini/job_agent/data/job_database.json"
urls_path = "/Users/chris/.gemini/tmp/chris/all_job_urls.txt"

with open(db_path, "r") as f:
    db = json.load(f)

existing_ids = set()
for entry in db:
    match = re.search(r'view/(\d+)', entry["url"])
    if match:
        existing_ids.add(match.group(1))

new_urls = []
if os.path.exists(urls_path):
    with open(urls_path, "r") as f:
        for line in f:
            url = line.strip()
            match = re.search(r'view/(\d+)', url)
            if match:
                job_id = match.group(1)
                if job_id not in existing_ids:
                    new_urls.append(f"https://www.linkedin.com/jobs/view/{job_id}/")
                    existing_ids.add(job_id) # Avoid duplicates in the same run

for url in new_urls:
    print(url)
