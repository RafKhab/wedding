import re

path = '/Users/rafaelkhabibullin/Documents/wedding-site/assets/images/промежуточный.svg'
with open(path, 'r') as f:
    content = f.read()

dx = 32.973

# Replace header
w_match = re.search(r'width="([\d\.]+)"', content)
h_match = re.search(r'height="([\d\.]+)"', content)
orig_h = float(h_match.group(1))

new_header = f'<svg width="1045" height="{orig_h}" viewBox="0 0 1045 {orig_h}" fill="none" xmlns="http://www.w3.org/2000/svg">\n<g transform="translate({dx}, 0)">\n'

path_start = content.find('<path')
path_end = content.find('</svg>')
inner = content[path_start:path_end]

new_content = new_header + inner + '</g>\n</svg>\n'

with open(path, 'w') as f:
    f.write(new_content)

print("Processed промежуточный.svg successfully.")
