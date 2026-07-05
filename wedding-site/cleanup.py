import re

path = '/Users/rafaelkhabibullin/Documents/wedding-site/index.html'
with open(path, 'r') as f:
    html = f.read()

# Grab the top part before content-layer
head_end = html.find('            <!-- Слой контента -->')
head_html = html[:head_end]

# Grab the bottom part after content-layer
tail_start = html.rfind('    <script src="script.js"></script>')
tail_html = '            </div>\n        </div>\n    </div>\n' + html[tail_start:]

# Extract first occurrence of each section precisely
def get_first_section(class_name):
    pattern = r'<section class="section ' + class_name + r'">.*?</section>'
    match = re.search(pattern, html, re.DOTALL)
    return match.group(0) if match else ''

save_the_date = get_first_section('save-the-date-section')
intro = get_first_section('intro-section')
location_full = get_first_section('location-section')
schedule = get_first_section('schedule-section')
palette = get_first_section('palette-section')
rsvp = get_first_section('rsvp-section')
footer_full = get_first_section('footer-section')

# Sometimes the footer might be inside location or its own section. Let's make sure we have it.
if not footer_full:
    # try extracting from location
    if '<div class="footer-signatures">' in location_full:
        parts = location_full.split('<div class="footer-signatures">')
        location = parts[0].strip() + '\n                </section>'
        footer_inner = '<div class="footer-signatures">' + parts[1].replace('</section>', '').strip()
        footer = f'''                <!-- 7. Футер -->
                <section class="section footer-section">
                    {footer_inner}
                </section>'''
    else:
        # maybe it's in a duplicated block, let's just regex for footer-signatures
        fs_match = re.search(r'<div class="footer-signatures">.*?</div>\s*</div>', html, re.DOTALL)
        location = location_full
        footer = f'''                <!-- 7. Футер -->
                <section class="section footer-section">
                    {fs_match.group(0)}
                </section>''' if fs_match else ''
else:
    location = location_full
    footer = footer_full

# In case location STILL has footer inside it (because of how we grabbed first occurrence)
if '<div class="footer-signatures">' in location:
    location = location.split('<div class="footer-signatures">')[0].strip() + '\n                </section>'

content_layer = f'''            <!-- Слой контента -->
            <div class="content-layer">
                
                <!-- 1. Главный экран -->
                {save_the_date}

                <!-- 2. Приглашение -->
                {intro}

                <!-- 3. Место проведения -->
                {location}

                <!-- 4. Расписание -->
                {schedule}

                <!-- 5. Палитра и Пожелания -->
                {palette}

                <!-- 6. RSVP Форма -->
                {rsvp}
                
                {footer}

'''

final_html = head_html + content_layer + tail_html

with open(path, 'w') as f:
    f.write(final_html)

print("HTML cleaned and rebuilt successfully!")
