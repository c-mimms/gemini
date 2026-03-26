import urllib.request
import urllib.parse
import json
import sys
import os

def fetch_image(query, output_path):
    # Search for page
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
    req = urllib.request.Request(search_url, headers={'User-Agent': 'BirthdayArchitectBot/2.0'})
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        if not data.get('query', {}).get('search'):
            print(f"No Wikipedia page found for '{query}'")
            return False
        title = data['query']['search'][0]['title']
        
        # Get image for page
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={urllib.parse.quote(title)}"
        req2 = urllib.request.Request(img_url, headers={'User-Agent': 'BirthdayArchitectBot/2.0'})
        response2 = urllib.request.urlopen(req2)
        data2 = json.loads(response2.read())
        
        pages = data2['query']['pages']
        page_id = list(pages.keys())[0]
        if 'original' not in pages[page_id]:
            print(f"No original image found for '{title}'")
            return False
            
        source = pages[page_id]['original']['source']
        
        # Download image
        print(f"Downloading {source} to {output_path}")
        req3 = urllib.request.Request(source, headers={'User-Agent': 'BirthdayArchitectBot/2.0'})
        response3 = urllib.request.urlopen(req3)
        with open(output_path, 'wb') as f:
            f.write(response3.read())
        print(f"Success: saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error fetching image: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 fetch_wiki_image.py 'Search Query' /path/to/output.jpg")
        sys.exit(1)
    fetch_image(sys.argv[1], sys.argv[2])
