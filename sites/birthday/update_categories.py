import os
import glob
mapping = {
    'Aviation Heritage': 'Aviation & Sightseeing',
    'Island Life': 'Nature & Gardens',
    'Private Serenity': 'Local Luxury',
    'Grounded Luxury': 'Local Luxury',
    'PNW Icon': 'Nature & Gardens',
    'Seasonal Bloom': 'Nature & Gardens',
    'Heritage Gift': 'Swedish Heritage',
    'Sentimental Project': 'Sentimental Experiences',
    'Swedish Design': 'Swedish Heritage',
    'Experience Gift': 'Sentimental Experiences',
    'PNW Luxury': 'Physical Keepsakes',
    'Custom Art': 'Custom Art',
    'Aviation Art': 'Custom Art',
    'PNW History': 'Physical Keepsakes',
    'Modern Heritage': 'Swedish Heritage'
}
for path in ['src/activities', 'src/gifts']:
    for f in glob.glob(f'/Users/chris/code/gemini/sites/birthday/{path}/*.html'):
        with open(f, 'r') as file: content = file.read()
        for old, new in mapping.items():
            content = content.replace(f'"{old}"', f'"{new}"')
            content = content.replace(f'>{old}<', f'>{new}<')
        with open(f, 'w') as file: file.write(content)
