#!/usr/bin/env python3
"""Add Dr. Anil Desai's photo to his testimonial card on:
- index.html (homepage testimonial section)
- All 15 enriched service & specialty pages
Idempotent.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENTINEL = '<!-- desai-photo-v1 -->'

# ─── Homepage update ────────────────────────────────────────────────────────
HOMEPAGE = os.path.join(ROOT, 'index.html')

HOMEPAGE_OLD = '<div class="testimonial-avatar">AD</div>'
HOMEPAGE_NEW = (
    '<div class="testimonial-avatar testimonial-avatar-photo">'
    '<img src="assets/dr-anil-desai-400.jpg" alt="Dr. Anil Desai" loading="lazy">'
    '</div>'
)

HOMEPAGE_CSS_ANCHOR = '.testimonial-avatar {'
HOMEPAGE_CSS_NEW = '''.testimonial-avatar-photo { background: none !important; padding: 0; overflow: hidden; }
.testimonial-avatar-photo img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; display: block; }
'''

# ─── Service/specialty page update ──────────────────────────────────────────
SVC_OLD = '''<figcaption class="testimonial-author">
        <div class="testimonial-name">Dr. Anil Desai, MD</div>
        <div class="testimonial-role">Multispecialty Surgical Center</div>
      </figcaption>'''
SVC_NEW = '''<figcaption class="testimonial-author testimonial-author--with-photo">
        <img class="testimonial-photo" src="../assets/dr-anil-desai-400.jpg" alt="Dr. Anil Desai" loading="lazy">
        <div class="testimonial-author-text">
          <div class="testimonial-name">Dr. Anil Desai, MD</div>
          <div class="testimonial-role">Multispecialty Surgical Center</div>
        </div>
      </figcaption>'''

SVC_CSS_ANCHOR = '.testimonial-author { border-top: 1px solid var(--line); padding-top: 18px; }'
SVC_CSS_NEW = '''.testimonial-author--with-photo { display: flex; align-items: center; gap: 14px; }
.testimonial-author--with-photo .testimonial-photo { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 2px solid var(--gold); display: block; }
.testimonial-author-text { flex: 1; }
'''


def update_homepage():
    with open(HOMEPAGE) as f: c = f.read()
    if SENTINEL in c:
        return 'SKIP homepage (already updated)'
    if HOMEPAGE_OLD not in c:
        return f'FAIL homepage: anchor {HOMEPAGE_OLD!r} not found'
    if HOMEPAGE_CSS_ANCHOR not in c:
        return 'FAIL homepage: CSS anchor not found'
    c = c.replace(HOMEPAGE_OLD, HOMEPAGE_NEW, 1)
    c = c.replace(HOMEPAGE_CSS_ANCHOR, HOMEPAGE_CSS_NEW + HOMEPAGE_CSS_ANCHOR, 1)
    c = c.replace('</title>', '</title>\n' + SENTINEL, 1) if SENTINEL not in c else c
    with open(HOMEPAGE, 'w') as f: f.write(c)
    return 'OK homepage'


def update_svc_page(path):
    with open(path) as f: c = f.read()
    if SENTINEL in c:
        return f'SKIP {path} (already updated)'
    if SVC_OLD not in c:
        return f'SKIP {path} (no Desai testimonial block in expected form)'
    if SVC_CSS_ANCHOR not in c:
        return f'FAIL {path}: CSS anchor not found'
    c = c.replace(SVC_OLD, SVC_NEW, 1)
    c = c.replace(SVC_CSS_ANCHOR, SVC_CSS_NEW + SVC_CSS_ANCHOR, 1)
    c = c.replace('</title>', '</title>\n' + SENTINEL, 1)
    with open(path, 'w') as f: f.write(c)
    return f'OK {path}'


if __name__ == '__main__':
    print(update_homepage())
    for d in ('services', 'specialties'):
        for p in sorted(glob.glob(os.path.join(ROOT, d, '*.html'))):
            print(update_svc_page(p))
