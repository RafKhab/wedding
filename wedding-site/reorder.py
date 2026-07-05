import re

with open('/Users/rafaelkhabibullin/Documents/wedding-site/index.html', 'r') as f:
    html = f.read()

# Extract each section
def extract_section(name):
    # Regex to find section by class
    # Assumes sections end with </section>
    pattern = r'<!-- \d+\. .*? -->\s*<section class="section ' + name + r'">.*?</section>'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        # Fallback if comment differs
        pattern2 = r'<section class="section ' + name + r'">.*?</section>'
        match = re.search(pattern2, html, re.DOTALL)
    return match.group(0) if match else ''

save_the_date = extract_section('save-the-date-section')
intro = extract_section('intro-section')
schedule = extract_section('schedule-section')
rsvp = extract_section('rsvp-section')
palette = extract_section('palette-section')

# Location section needs special handling because it contains footer-signatures
location_full = extract_section('location-section')
# Split location_full into location and footer
footer_split_str = r'<div class="footer-signatures">'
parts = location_full.split(footer_split_str)
location = parts[0].strip() + '\n                </section>'

footer = '''                <!-- 7. Футер -->
                <section class="section footer-section">
                    <div class="footer-signatures">''' + parts[1].replace('</section>', '').strip() + '''
                </section>'''

# Combine in new order
new_content_layer = f'''            <!-- Слой контента -->
            <div class="content-layer">
                
{save_the_date}

{intro}

{location}

{schedule}

{palette}

{rsvp}

{footer}

            </div>'''

# Replace old content-layer
pattern_full = r'            <!-- Слой контента -->\s*<div class="content-layer">.*?</div>\s*</div>\s*</div>\s*<script src="script.js"></script>'

# We need to be careful with the outer divs
start_idx = html.find('            <!-- Слой контента -->\n            <div class="content-layer">')
end_idx = html.find('            </div>\n        </div>\n    </div>\n    <script src="script.js"></script>')

new_html = html[:start_idx] + new_content_layer + '\n' + html[end_idx:]

with open('/Users/rafaelkhabibullin/Documents/wedding-site/index.html', 'w') as f:
    f.write(new_html)

print("Reordered successfully!")
