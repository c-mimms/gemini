import os
import sys
import datetime
import urllib.request
import imghdr
import traceback
import re

ROOT = "/Users/chris/code/gemini"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from simple_generator.core import generate_structured
from simple_generator.examples.museum.schema import MuseumArticle

MUSEUM_ARTICLES_DIR = "/Users/chris/code/gemini/discord_bot/scripts/museum_articles"
IMAGES_DIR = os.path.join(MUSEUM_ARTICLES_DIR, "images")

def download_image_robust(url: str, output_path: str, timeout: int = 15) -> bool:
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "MimmsMuseumBot/1.0 (https://mimmsmuseum.org; contact@yourdomain.com)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        
        with open(output_path, "wb") as f:
            f.write(data)

        # Verify it's actually an image, not a blocked HTML page
        image_type = imghdr.what(output_path)
        if image_type is None:
            os.remove(output_path)
            print(f"Failed: Not a valid image -> {url}")
            return False
            
        return True
    except Exception as e:
        print(f"Failed: Exception downloading {url} -> {e}")
        return False

def main():
    instructions_path = os.path.join(os.path.dirname(__file__), "museum_instructions.md")
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    print("Generating museum article...")
    # Instruct the LLM to pick a format and an artifact randomly and create the article.
    user_prompt = (
        "Please randomly choose ONE of the 9 formats described in the instructions, "
        "and pick an artifact, theme, or person from the history of computing. "
        "Research it implicitly and generate a deeply detailed, compelling article satisfying the schema. "
        "Provide your output purely as JSON."
    )

    try:
        # Defaulting to a strong model for complex structured output
        model_name = os.getenv("GENERATOR_MODEL", "gemini-2.5-flash")
        article: MuseumArticle = generate_structured(
            instructions=instructions,
            user_prompt=user_prompt,
            response_schema=MuseumArticle,
            model_name=model_name
        )
    except Exception as e:
        print(f"Error during generation: {e}")
        traceback.print_exc()
        sys.exit(1)

    print(f"Generated Topic: {article.topic_or_artifact}")
    print(f"Format Used  : {article.format_used}")
    
    # Process Images
    if article.image_urls_to_download:
        print(f"Found {len(article.image_urls_to_download)} image URLs to download.")
        for url in article.image_urls_to_download:
            filename = os.path.basename(url.split("?")[0])
            if not filename or filename.startswith("Special:"):
                # fallback for weird URLs
                filename = f"image_{hash(url)}.jpg"
            
            output_path = os.path.join(IMAGES_DIR, filename)
            resolved = download_image_robust(url, output_path)
            if resolved:
                print(f" -> Downloaded: {filename}")
                # Replace the remote URL with the local reference in the html_content
                article.html_content = article.html_content.replace(url, f"images/{filename}")

    # Build the final HTML Payload with metadata wrapper
    metadata_block = f'''
<div class="metadata" style="display:none;">
    <meta name="title" content="{article.title}">
    <meta name="description" content="{article.description}">
    <meta name="tag" content="{article.tag}">
</div>
'''
    final_html = f'<main class="museum-body">\n{metadata_block}\n{article.html_content}\n</main>'

    # Save to file
    date_str = datetime.date.today().isoformat()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", article.topic_or_artifact.lower()).strip("-")
    if not slug:
        slug = "museum-article"
    
    filename = f"{date_str}_{slug[:80]}.html"
    os.makedirs(MUSEUM_ARTICLES_DIR, exist_ok=True)
    out_path = os.path.join(MUSEUM_ARTICLES_DIR, filename)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"\nSuccess! Saved to {out_path}")

if __name__ == "__main__":
    main()
