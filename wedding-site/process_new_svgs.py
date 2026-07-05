import os
import re

offsets = {
    '1.svg': 25.0,
    '3.svg': 6.21
}

for filename, dx in offsets.items():
    path = f'/Users/rafaelkhabibullin/Documents/wedding-site/assets/images/{filename}'
    with open(path, 'r') as f:
        content = f.read()
    
    # Extract original dimensions
    w_match = re.search(r'width="([\d\.]+)"', content)
    h_match = re.search(r'height="([\d\.]+)"', content)
    orig_w = float(w_match.group(1))
    orig_h = float(h_match.group(1))
    
    # Replace the svg header
    new_header = f'<svg width="1045" height="{orig_h}" viewBox="0 0 1045 {orig_h}" fill="none" xmlns="http://www.w3.org/2000/svg">\n<g transform="translate({dx}, 0)">\n'
    
    # find the path
    path_start = content.find('<path')
    path_end = content.find('</svg>')
    inner = content[path_start:path_end]
    
    new_content = new_header + inner + '</g>\n</svg>\n'
    
    with open(path, 'w') as f:
        f.write(new_content)

print("Processed 1.svg and 3.svg successfully.")
