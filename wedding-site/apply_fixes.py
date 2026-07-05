import re

# 1. Update index.html
with open('/Users/rafaelkhabibullin/Documents/wedding-site/index.html', 'r') as f:
    html = f.read()

# Increase 1.15em to 1.25em
html = html.replace('1.15em', '1.25em')

# Move contact-organizer
contact_org_pattern = r'\s*<div class="contact-organizer">.*?</div>\s*</div>'
match = re.search(contact_org_pattern, html, re.DOTALL)
if match:
    contact_block = match.group(0)
    # Remove from original place
    html = html.replace(contact_block, '')
    
    # We need to strip the extra trailing </div> which belonged to .contact-organizer?
    # Wait, the regex captures a second </div>? Let's check the HTML.
    '''
                    <div class="contact-organizer">
                        ...
                        <div class="social-buttons">
                            <a>...</a>
                            <a>...</a>
                        </div>
                    </div>
    '''
    # So it ends with </div>\n                    </div>
    contact_block_clean_pattern = r'\s*<div class="contact-organizer">.*?</svg>\s*</a>\s*</div>\s*</div>'
    match = re.search(contact_block_clean_pattern, html, re.DOTALL)
    if match:
        contact_block = match.group(0)
        html = html.replace(contact_block, '')
        
        # Insert before footer
        footer_pattern = r'\s*<section class="section footer-section">'
        html = html.replace('<section class="section footer-section">', 
                            '<section class="section contact-section">' + contact_block + '\n                </section>\n                \n                <section class="section footer-section">')

# Modify footer
old_footer = '''<div class="footer-signatures"><h2 class="cursive-text">Будем рады вас видеть !</h2>
                        <div class="divider-line"></div>
                        <h1 class="footer-names">Гульназ & Рафа<span style="font-size: 1.25em">э</span>ль</h1>
                    </div>'''

new_footer = '''<div class="footer-signatures">
                        <div class="divider-line"></div>
                        <h2 class="cursive-text">Будем рады вас видеть !</h2>
                    </div>'''

html = html.replace(old_footer, new_footer)

with open('/Users/rafaelkhabibullin/Documents/wedding-site/index.html', 'w') as f:
    f.write(html)

# 2. Update styles.css
with open('/Users/rafaelkhabibullin/Documents/wedding-site/styles.css', 'r') as f:
    css = f.read()

# content-layer padding
css = css.replace('padding: 40px 20px;', 'padding: 40px 10px 40px 30px;')

# section-title centering
if 'text-align: center;' not in css.split('.section-title {')[1].split('}')[0]:
    css = css.replace('.section-title {\n    font-family: var(--font-serif);', '.section-title {\n    font-family: var(--font-serif);\n    text-align: center;')

# intro-text centering
if 'text-align: center;' not in css.split('.intro-text {')[1].split('}')[0]:
    css = css.replace('.intro-text {\n    font-size: 15px;', '.intro-text {\n    font-size: 15px;\n    text-align: center;')

# address-text centering
if 'text-align: center;' not in css.split('.address-text {')[1].split('}')[0]:
    css = css.replace('.address-text {\n    font-size: 16px;', '.address-text {\n    font-size: 16px;\n    text-align: center;')

# palette-desc, wishes-desc centering
if 'text-align: center;' not in css.split('.palette-desc, .wishes-desc {')[1].split('}')[0]:
    css = css.replace('.palette-desc, .wishes-desc {\n    font-size: 14px;', '.palette-desc, .wishes-desc {\n    font-size: 14px;\n    text-align: center;')

# schedule-list positioning
css = css.replace('.schedule-list {\n    margin: 30px 0;\n}', '.schedule-list {\n    width: 80%;\n    margin: 30px auto;\n}')

with open('/Users/rafaelkhabibullin/Documents/wedding-site/styles.css', 'w') as f:
    f.write(css)

print("Updates applied successfully!")
