import os

with open('/Users/rafaelkhabibullin/Documents/wedding-site/assets/images/3.svg', 'r') as f:
    c3 = f.read()

with open('/Users/rafaelkhabibullin/Documents/wedding-site/assets/images/4.svg', 'r') as f:
    c4 = f.read()

def get_g(content):
    start = content.find('<g')
    end = content.find('</g>') + 4
    return content[start:end]

g3 = get_g(c3)
g4 = get_g(c4)

import re
# Shift g4 down by exactly 625.5 to remove the 0.5px overlap
g4 = re.sub(r'translate\(([\d\.]+), 0\)', r'translate(\1, 625.5)', g4)

# Total height becomes 1251
new_svg = f'<svg width="1129" height="1251" viewBox="0 0 1129 1251" fill="none" xmlns="http://www.w3.org/2000/svg">\n{g3}\n{g4}\n</svg>'

with open('/Users/rafaelkhabibullin/Documents/wedding-site/assets/images/3_4_combined.svg', 'w') as f:
    f.write(new_svg)

print("Created 3_4_combined.svg with no overlap")
