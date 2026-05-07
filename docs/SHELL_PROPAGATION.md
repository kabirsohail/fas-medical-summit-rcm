# Shell Propagation — How to Update Shared Elements

The site has 24 self-contained HTML files. Each one has its own `<head>`, `<nav>`, contact strip, mobile menu, and `<footer>`. When you change a shared element, you must propagate the change across all 24 pages.

## Why this approach (and why it's intentional)

1. **No build step.** Drop any HTML file into a browser — works.
2. **Easy WordPress migration.** When migrating to WP, the shared shell becomes `header.php` / `footer.php` cleanly.
3. **Page-level overrides are easy.** Need a different nav for the legal pages? Just edit those pages.
4. **Tradeoff:** Shared changes need a propagation script.

## The propagation pattern

When you change anything in the shared shell, write a Python script that does string-replace across all 24 files. Pattern:

```python
import os, glob

ROOT = '.'  # or the absolute path to the project

OLD = """<old HTML block exactly as it appears>"""

NEW = """<new HTML block>"""

count = 0
for path in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    with open(path) as f:
        content = f.read()
    if OLD in content:
        content = content.replace(OLD, NEW)
        with open(path, 'w') as f:
            f.write(content)
        count += 1
        print(f'  ✓ {os.path.relpath(path, ROOT)}')

print(f'\nUpdated {count} files')
```

**Key rules:**
- Use exact-match string replace, not regex (regex breaks easily on whitespace)
- Run on a clean git working tree so you can `git diff` the result
- Always run the integrity check afterward (see below)

## What lives in the shared shell

### Top contact strip (38px tall, fixed)

```html
<!-- Top contact strip -->
<div class="contact-strip" role="region" aria-label="Contact information">
  <div class="contact-strip-inner">
    <div class="contact-strip-left">
      <a href="tel:9722945716" class="contact-strip-item">...</a>
      <span class="contact-strip-divider"></span>
      <a href="mailto:info@fasmedicalsummitrcm.com" class="contact-strip-item">...</a>
    </div>
    <div class="contact-strip-right">
      <span class="contact-strip-pulse"></span>
      <span>Free 30-min consultation · 24-hr response</span>
    </div>
  </div>
</div>
```

### Main nav (top: 38px)

```html
<nav class="nav" id="nav">
  <div class="nav-inner">
    <a href="index.html" class="logo" aria-label="FAS Medical Summit Home">
      <div class="logo-mark" aria-hidden="true">
        <span class="logo-shine"></span>
      </div>
      <div class="logo-text">
        <strong>FAS Medical Summit</strong>
        <small>REVENUE CYCLE MANAGEMENT · <span class="gold-rcm">RCM</span></small>
      </div>
    </a>
    <div class="nav-menu">
      <a href="index.html" class="nav-item">Home</a>
      <!-- Services dropdown -->
      <!-- Specialties dropdown -->
      <a href="about.html" class="nav-item">About</a>
      <a href="#reviews" class="nav-item">Reviews</a>
      <a href="insights.html" class="nav-item">Blogs</a>
      <a href="#faq" class="nav-item">FAQ</a>
      <a href="contact.html" class="nav-cta">Free Consultation →</a>
    </div>
    <button class="hamburger">...</button>
  </div>
</nav>
```

### Mobile menu drawer

```html
<div class="mobile-menu-overlay" id="mobile-menu-overlay"></div>
<div class="mobile-menu" id="mobile-menu">
  <!-- ...sections of links... -->
</div>
```

### Footer

```html
<footer>
  <div class="container footer-grid">
    <!-- Brand column -->
    <!-- Services column -->
    <!-- Specialties column -->
    <!-- Company column -->
  </div>
  <div class="footer-bottom">
    <span>© 2026 FAS Medical Summit, Inc. ...</span>
    <!-- Privacy / Terms / HIPAA links -->
  </div>
</footer>
```

## Sub-page link fixup

Pages in `/services/` and `/specialties/` need `../` prefixes on all internal links. When propagating shell changes to sub-pages, either:

1. Maintain two versions of the shell (root-page version + sub-page version with `../` prefixes), OR
2. Run a follow-up regex pass on sub-pages:

```python
# After propagating, fix paths in services/ and specialties/ subpages:
import re, glob, os

for path in glob.glob('services/*.html') + glob.glob('specialties/*.html'):
    with open(path) as f: c = f.read()
    # Fix relative paths to be ../ prefixed
    c = re.sub(r'href="(?!http|mailto:|tel:|#|\.\./|/)([\w\-]+\.html)', r'href="../\1', c)
    c = re.sub(r'href="services/', r'href="../services/', c)
    c = re.sub(r'href="specialties/', r'href="../specialties/', c)
    with open(path, 'w') as f: f.write(c)
```

## Integrity check (run after every propagation)

```python
import os, re

all_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            all_files.append(os.path.relpath(os.path.join(root, f)))

tag_issues = broken_links = dead_hash = 0
all_set = set(all_files)
fids = {p: set(re.findall(r'\sid="([^"]+)"', open(p).read())) for p in all_files}

for p in all_files:
    c = open(p).read()
    d = os.path.dirname(p)
    for tag in ['section','div','a','button','form','script','style','svg']:
        o = len(re.findall(r'<' + tag + r'[\s>]', c))
        cl = len(re.findall(r'</' + tag + r'>', c))
        if o != cl:
            tag_issues += 1
            print(f'  ✗ {p}: <{tag}> imbalance ({o} open vs {cl} close)')
    for link in re.findall(r'href="([^"]+)"', c):
        if link.startswith(('http','mailto:','tel:')) or link == '#': continue
        po = link.split('#')[0].split('?')[0]
        if po and po.endswith('.html'):
            r = os.path.normpath(os.path.join(d, po))
            if r not in all_set:
                broken_links += 1
                print(f'  ✗ {p}: broken link → {link}')
    dead_hash += c.count('href="#"')

print(f'\nTag balance:    {tag_issues}')
print(f'Broken links:   {broken_links}')
print(f'Dead # links:   {dead_hash}')
print(f'\nShould all be 0.')
```

## Examples of past propagations

### Renaming "Insights" → "Blogs" across all 24 pages

```python
patterns = [
    ('class="nav-item">Insights</a>', 'class="nav-item">Blogs</a>'),
    ('<li><a href="insights.html">Insights</a></li>',
     '<li><a href="insights.html">Blogs</a></li>'),
    # ...etc
]

for path in glob.glob('**/*.html', recursive=True):
    with open(path) as f: c = f.read()
    for old, new in patterns:
        c = c.replace(old, new)
    with open(path, 'w') as f: f.write(c)
```

### Changing the phone number

```python
OLD_TEL = '972-294-5716'
NEW_TEL = '972-555-0123'

OLD_HREF = 'tel:9722945716'
NEW_HREF = 'tel:9725550123'

for path in glob.glob('**/*.html', recursive=True):
    with open(path) as f: c = f.read()
    c = c.replace(OLD_TEL, NEW_TEL).replace(OLD_HREF, NEW_HREF)
    with open(path, 'w') as f: f.write(c)
```

### Adding a new service to the dropdown

When adding `services/new-service.html`, the dropdown link must be added to:
- The Services dropdown nav (in all 24 pages)
- The mobile menu Services list
- The footer Services column

Use `'<a href="services/credentialing.html"'` as your anchor — the new service link goes after that one (or wherever fits the order).

## Page-level overrides

Some pages need slight nav variations:
- Legal pages (privacy, terms, hipaa) might want a simplified nav
- Service / specialty detail pages have current-page styling on their parent dropdown

When propagating, check the diff carefully. Don't blindly overwrite a page that has intentional variation.
