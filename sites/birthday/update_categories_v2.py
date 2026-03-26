import os
import glob
mapping = {
    'Aviation & Sightseeing': 'Exploration',
    'Nature & Gardens': 'Exploration',
    'Local Luxury': 'Relaxation',
    'Swedish Heritage': 'Keepsakes',
    'Sentimental Experiences': 'Experiences',
    'Physical Keepsakes': 'Keepsakes',
    'Custom Art': 'Art & Decor'
}
for path in ['src/activities', 'src/gifts']:
    for f in glob.glob(f'/Users/chris/code/gemini/sites/birthday/{path}/*.html'):
        with open(f, 'r') as file: content = file.read()
        for old, new in mapping.items():
            content = content.replace(f'"{old}"', f'"{new}"')
            content = content.replace(f'>{old}<', f'>{new}<')
        with open(f, 'w') as file: file.write(content)
