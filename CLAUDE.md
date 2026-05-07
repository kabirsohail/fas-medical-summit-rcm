# Claude Code — FAS Medical Summit Project Context

This file is loaded into Claude Code's context when you open this folder. It contains the rules, decisions, and constraints that should guide every change.

## What this project is

A custom marketing website for **FAS Medical Summit RCM** (medical billing & RCM company in Frisco, Texas). The site is for surgical specialty prospects — ASCs, anesthesiologists, pain management, cardiology, emergency medicine, family practice. Owners are friends of the user; this is a real business with a struggling post-NSA pivot, ~1,000 employees in India, building toward AI-driven efficiency.

## User context

- **The user is non-technical.** They cannot make project-management or technical decisions. Drive the work; don't ask permission for every step.
- **The user wants Claude to be the senior dev** — make decisions, execute, then summarize what was done.
- **Owners may audit prospects' claims** — every number on the site must be defensible.

## Critical rules

### NEVER violate these

1. **No fabricated "live" data.** No tickers that imply real-time operational data. No "$X processed today" with animated counters. No "● LIVE" indicators.
2. **No unverified specific claims.** If a number isn't on the canonical data sheet (below), label it "EXAMPLE" or remove it.
3. **No "real-time dashboards" claims** unless verified — soften to "transparent reporting" or "continuously-updated reporting." Exception: "Real-time 270/271 eligibility verification" is fine (it's literally an EDI standard).
4. **No promise words** that create legal exposure: "always," "guaranteed," "we promise," "never lose."
5. **No fabricated client logos / testimonials.** The 3 named physicians (Dr. Adeel Haq, Dr. Jessen Mukalel, Dr. Anil Desai) are real and verified — don't add others without verification.
6. **Headings stay clean.** No headline-skipping (h1 → h3 is OK, h1 → h4 is not). Footer h3 is preserved as h3 (we already migrated from h4).

### Canonical FAS data (verified — use freely)

| Metric | Value |
|---|---|
| Company formed | 2022 |
| Owner medical billing experience | 25+ years |
| Team size | 450+ specialists |
| Total billing value processed | $2.7B (since 2022) |
| First-pass acceptance rate | **96%** (NEVER 99.8%) |
| Average A/R days | 32 |
| Active clients | 200 |
| Ongoing projects | 50 |
| Client revenue growth | up to 30% |
| Coding department | 150+ certified coders |
| Transaction Processing dept | 200+ |
| A/R Management dept | 100+ |
| Address | 400 Stonebrook Parkway, Suite 1104, Frisco, Texas 75036 |
| Phone | 972-294-5716 |
| Email | info@fasmedicalsummitrcm.com |
| Website domain | fasmedicalsummitrcm.com |

### Stats currently used that need owner verification before launch

These appear on individual service/specialty pages. If FAS confirms, leave; otherwise soften:
- 78% IDR win rate (emergency-medicine page)
- 67% appeal win rate (denial-management page)
- 94% prior authorization approval (pain-management page)
- 74% patient collection rate (patient-billing page)
- 38% denial reduction in 90 days (patient-onboarding page)
- 99% coding accuracy (charge-capture-coding page)

## Design system

See `docs/DESIGN_SYSTEM.md` for full tokens. Quick reference:

```
Colors:
  --bg-deep:     #0A1220    (page background)
  --bg-surface:  #0F1A2E    (raised surface)
  --bg-elevated: #15233D    (cards, panels)
  --gold:        #C9A961    (accent — primary)
  --gold-bright: #E5C97D    (accent — hover/highlight)
  --gold-deep:   #8F6D2F    (accent — gradient end)
  --ink-primary: #F4EFE6    (cream — body text)
  --ink-secondary: #B8B0A0   (muted body text)
  --ink-tertiary: #7A8090   (labels, metadata)
  --crimson:     #B85450    (alerts, warnings)
  --emerald:     #4A7C6F    (success, positive)
  --line:        rgba(244, 239, 230, 0.08)   (borders)
  --line-strong: rgba(244, 239, 230, 0.14)

Fonts:
  --serif: 'Fraunces', Georgia, serif       (display, h1-h3)
  --sans:  'Plus Jakarta Sans', system-ui  (body, UI)
  --mono:  'JetBrains Mono', monospace     (eyebrows, labels, numbers)

Spacing: 4px / 8px / 12px / 16px / 24px / 32px / 48px / 80px / 120px / 160px

Radii:
  --radius-sm: 8px     (small inputs, badges)
  --radius-md: 14px    (medium cards)
  --radius-lg: 18px    (large cards, sections)

Easing:
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1)
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)
```

## Architecture decisions (locked in)

1. **All CSS and JS is inlined** in each HTML file. This is intentional — no build step, easy WordPress migration, page-by-page edits possible. Don't refactor to external stylesheets without a strong reason.

2. **Each of the 24 pages is self-contained.** They share the same `<head>` block + `<nav>` + `<footer>` shell, so a change to those needs to propagate to all 24 pages. Use a Python script (see `docs/SHELL_PROPAGATION.md`) when changing shared elements.

3. **No JavaScript frameworks.** Pure vanilla JS. The user is non-technical and the next dev to touch this might be a WordPress dev — keep it simple.

4. **No image files yet** — every visual is hand-coded SVG, every blog "image" is an inline SVG illustration. This is also intentional. When you replace with photos later, swap the SVG block for an `<img>` tag.

5. **Reveal-on-scroll animations** use IntersectionObserver. Cards have `class="reveal"` and animate in when 20% visible.

6. **3D effects** use CSS `transform-style: preserve-3d` + `perspective` on parent. Mouse-tracking uses CSS custom properties (`--mx`, `--my`, `--rx`, `--ry`) updated via JS.

## Tone and voice

- Confident but not boastful
- Specific over vague — "32-day A/R" beats "fast turnaround"
- No corporate jargon ("synergize," "leverage cutting-edge," "world-class solutions")
- Uses sentence case in most headings (Title Case is reserved for true proper nouns)
- Prefers em-dashes (—) over double-hyphens, curly quotes over straight quotes in body copy

Read `docs/CONTENT_GUIDELINES.md` for the full voice guide.

## Common tasks and how to do them

### Adding a new service or specialty page
1. Copy an existing one (e.g., `services/patient-onboarding.html`) as the template
2. Update meta tags (title, description, canonical, OG, JSON-LD)
3. Update content sections
4. Add the new page to:
   - Homepage services dropdown nav
   - Mobile menu services list
   - Footer "Services" column
   - Sitemap (when one exists)

### Editing the contact strip, nav, or footer
This appears on all 24 pages. Don't edit one page — write a Python script that propagates the change. Pattern:

```python
import os, glob
for path in glob.glob('**/*.html', recursive=True):
    with open(path) as f: c = f.read()
    c = c.replace('OLD STRING', 'NEW STRING')
    with open(path, 'w') as f: f.write(c)
```

### Adding a new homepage section
- New sections go in `index.html` only
- Must use existing design tokens (colors, fonts, spacing)
- Should have a matching mobile breakpoint (640px and 1024px are the existing breakpoints)
- If interactive, must have `prefers-reduced-motion` fallback

### Removing a fabricated number
1. Find every place it appears: `grep -rn "the number" .`
2. Replace with verified canonical data OR clearly label as "EXAMPLE"
3. Run integrity check (see below)

### Running the integrity check

After ANY edit, verify nothing broke:

```bash
python3 -c "
import os, re
all_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            all_files.append(os.path.relpath(os.path.join(root, f)))

tag_issues = broken_links = dead_hash = 0
all_set = set(all_files)
fids = {p: set(re.findall(r'\sid=\"([^\"]+)\"', open(p).read())) for p in all_files}

for p in all_files:
    c = open(p).read()
    d = os.path.dirname(p)
    for tag in ['section','div','a','button','form','script','style']:
        o = len(re.findall(r'<' + tag + r'[\s>]', c))
        cl = len(re.findall(r'</' + tag + r'>', c))
        if o != cl: tag_issues += 1
    for link in re.findall(r'href=\"([^\"]+)\"', c):
        if link.startswith(('http','mailto:','tel:')) or link == '#': continue
        po = link.split('#')[0].split('?')[0]
        if po and po.endswith('.html'):
            r = os.path.normpath(os.path.join(d, po))
            if r not in all_set: broken_links += 1
    dead_hash += c.count('href=\"#\"')

print(f'Tag balance:    {tag_issues}')
print(f'Broken links:   {broken_links}')
print(f'Dead # links:   {dead_hash}')
"
```

Should print all zeros. Anything else = something broke.

## Pending pre-launch tasks

See `docs/PENDING_TASKS.md` — the prioritized launch checklist.

## When in doubt

- **Default toward defensible.** Vague-but-true beats specific-but-fabricated.
- **Default toward simple.** This site will be maintained by someone less skilled than Claude. No clever tricks.
- **Default toward consistency.** If a pattern exists elsewhere on the site, follow it. Don't invent new patterns.
- **Default toward action.** The user is non-technical and explicitly wants Claude to drive work. Don't ask "should I do X or Y?" when one option is clearly better — just do it and explain.
