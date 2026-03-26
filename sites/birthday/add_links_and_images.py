import os
import glob
import subprocess

gifts_to_fetch = {
    'captains_log_journal.html': 'Leather',
    'filson_rugged_tote.html': 'Tote bag',
    'georg_jensen_daisy.html': 'Daisy',
    'last_hurrah_photoshoot.html': 'Camera',
    'mt_st_helens_glass_art.html': 'Glass art',
    'puget_sound_topo_map.html': 'Topographic map',
    'svenskt_tenn_pewter.html': 'Pewter'
}

repo_root = "/Users/chris/code/gemini"
gift_dir = os.path.join(repo_root, "sites/birthday/src/gifts")
act_dir = os.path.join(repo_root, "sites/birthday/src/activities")

# 1. Fetch images for gifts
for filename, search_term in gifts_to_fetch.items():
    filepath = os.path.join(gift_dir, filename)
    img_name = filename.replace('.html', '.jpg')
    img_dest = os.path.join(repo_root, f"sites/birthday/data/images/{img_name}")
    
    # fetch image
    subprocess.run(["python3", os.path.join(repo_root, "agent_tools/fetch_wiki_image.py"), search_term, img_dest])
    
    # inject image into html if not there
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            html = f.read()
        if '<img src' not in html:
            img_tag = f'\n    <img src="/data/images/{img_name}" alt="{search_term}">\n'
            # insert after </h3>
            html = html.replace('</h3>', f'</h3>{img_tag}')
            with open(filepath, 'w') as f:
                f.write(html)

# 2. Inject btn-outline links into ALL FILES
for dir_path in [gift_dir, act_dir]:
    for filepath in glob.glob(os.path.join(dir_path, "*.html")):
        with open(filepath, 'r') as f:
            html = f.read()
        if 'btn-outline' not in html:
            btn_raw = '\n    <a href="#" class="btn-outline">View Details</a>\n'
            # insert before the final </div> which closes .editorial-item
            last_div_idx = html.rfind('</div>')
            if last_div_idx != -1:
                html = html[:last_div_idx] + btn_raw + html[last_div_idx:]
            with open(filepath, 'w') as f:
                f.write(html)
