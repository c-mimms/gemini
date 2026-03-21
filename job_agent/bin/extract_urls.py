import json
import re
import sys

def extract_urls(email_data):
    body = email_data.get("body", "")
    html_body = email_data.get("html_body", "")
    
    # Extract from plain text body
    # Pattern: https://www.linkedin.com/comm/jobs/view/JOB_ID/
    urls = re.findall(r'https://www.linkedin.com/comm/jobs/view/\d+[^ \n\r\t]*', body)
    
    # Extract from HTML body if needed (often more complete)
    html_urls = re.findall(r'https://www.linkedin.com/comm/jobs/view/\d+[^"\' \n\r\t]*', html_body)
    
    return list(set(urls + html_urls))

if __name__ == "__main__":
    content = sys.stdin.read()
    # Try to find all JSON objects in the content
    # This is a bit hacky but should work for a sequence of { ... } { ... }
    all_urls = []
    
    # Attempt to parse as a single JSON object first
    try:
        data = json.loads(content)
        if isinstance(data, list):
            for item in data:
                all_urls.extend(extract_urls(item))
        else:
            all_urls.extend(extract_urls(data))
    except json.JSONDecodeError:
        # Fallback: try to split by }{ and parse each
        # Or just use regex to find URLs in the whole content
        urls = re.findall(r'https://www.linkedin.com/comm/jobs/view/\d+[^"\' \n\r\t& ]*', content)
        all_urls.extend(urls)
    
    # Unique URLs
    # Filter out tracker fragments like &trk=... if they are too long, 
    # but LinkedIn comm links often need them for redirects.
    # We want the direct link if possible.
    
    unique_urls = set()
    for url in all_urls:
        # Clean up URL (remove trailing punctuation or escapes)
        url = url.split('\\')[0] # Remove JSON escape backslashes
        url = url.split('"')[0]
        url = url.split("'")[0]
        if url.endswith('.') or url.endswith(','):
            url = url[:-1]
        unique_urls.add(url)
    
    for url in sorted(list(unique_urls)):
        print(url)
