# Pending Tasks — Launch Checklist

The site is structurally complete and visually polished. These are the items between "looks great" and "live on fasmedicalsummitrcm.com."

## Critical (blocks launch)

### 1. og-image.png does not exist

Every page references `https://fasmedicalsummitrcm.com/og-image.png` in the OG meta tags. This image needs to be created before launching, otherwise social shares will look broken.

**Spec:**
- 1200 × 630 pixels
- PNG (or JPG, but PNG is safer for the gradient-heavy design)
- Should match site aesthetic: dark navy bg, gold accents, FAS Medical Summit logo
- Recommended copy: "FAS Medical Summit — Revenue Cycle Excellence for Surgical Specialties"

**How to create:** Canva, Figma, Photoshop. Or Claude can hand-build an SVG with the right composition and the user can screenshot/export.

**Place at:** `assets/og-image.png` (then update site to reference `/assets/og-image.png` or move to root).

### 2. Form backend wired

Completed May 7, 2026. This no longer blocks launch.

Both the homepage Free Consultation form and `contact.html` form now POST to `/api/lead`.

Current behavior:
- Validates required name, email, and phone server-side
- Uses a honeypot field to silently discard obvious bot submissions
- Stores each real submission as a private Vercel Blob JSON record at `leads/YYYY-MM-DD/<lead-id>.json`
- Logs each lead in Vercel Function logs as a fallback
- Sends email notifications through Resend when `RESEND_API_KEY` is added

The private Vercel Blob store `fas-leads` is connected to the Vercel project. Optional remaining setup: add `RESEND_API_KEY` if the owners want every lead emailed to `info@fasmedicalsummitrcm.com` immediately.

### 3. Owner verification of unverified stats

These stats appear on service/specialty pages but haven't been confirmed by FAS leadership:

- 78% IDR win rate — `specialties/emergency-medicine.html`
- 67% appeal win rate — `services/denial-management.html`
- 94% prior auth approval — `specialties/pain-management.html`
- 74% patient collection rate — `services/patient-billing.html`
- 38% denial reduction in 90 days — `services/patient-onboarding.html`
- 99% coding accuracy — `services/charge-capture-coding.html`

**Action:** Send to FAS leadership for confirmation. If they confirm: leave. If they don't: soften the language (e.g., "high IDR win rate") or remove entirely.

## Important (should fix before launch but not strictly required)

### 4. sitemap.xml + robots.txt

Search engines need these for clean indexing.

**sitemap.xml** — list all 24 pages with their priorities:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://fasmedicalsummitrcm.com/</loc><priority>1.0</priority></url>
  <url><loc>https://fasmedicalsummitrcm.com/about.html</loc><priority>0.8</priority></url>
  <!-- ... all 24 pages -->
</urlset>
```

**robots.txt:**
```
User-agent: *
Allow: /
Sitemap: https://fasmedicalsummitrcm.com/sitemap.xml
```

### 5. Real client logos

The Trust Strip section names some clients but doesn't have logos. Either:
- Get permission from FAS clients to use their logos
- Replace with greyscale text-only ("As trusted by surgical practices in TX, NY, FL...")

### 6. Real leadership photos

The About page has placeholder avatars (initials in circles). Real headshots would significantly upgrade the credibility — even basic professional headshots from the 2-3 senior leaders.

### 7. Individual blog post pages

Currently `insights.html` lists 10 blog topics with illustrations and excerpts, but clicking a card doesn't go anywhere (no individual article pages exist yet). Either:
- Build out 10 article pages (significant content writing effort)
- Mark cards as "Coming soon" until content is ready
- Link to external resources (e.g., FAS LinkedIn posts) for now

## Nice to have

### 8. Real photos in services / specialty hero areas

Currently each detail page has a clean dark hero. Topical photography (anesthesiologists at work, ASC operating rooms, billing operations centers) would warm up the pages — but only if they're high-quality and on-brand. Stock photos that look stock will hurt more than help.

### 9. Browser testing

The site's been validated structurally (tags, links, anchors all clean) but hasn't been manually tested in:
- Chrome desktop, Firefox, Safari (different rendering engines)
- iOS Safari, Chrome Android (real device touch behavior)
- Older Chrome versions (some businesses still use Chrome 80+)
- Print stylesheets (someone WILL print the contact page)

### 10. Performance audit

Each homepage is ~227 KB which is fine for a marketing site, but worth running:
- Lighthouse audit (Chrome DevTools → Lighthouse)
- WebPageTest.org
- Look for any 3D animations causing jank on lower-end Android

### 11. Analytics

No analytics tracker currently installed. Recommended:
- Google Analytics 4 (free, requires GA snippet in `<head>`)
- Or Plausible / Fathom (privacy-friendly, paid)

### 12. CRM integration

When form backend is wired (item #2), connect leads directly to FAS's CRM (HubSpot? Salesforce? Pipedrive?) so prospects don't sit in an inbox.

## Deployment options (in order of recommendation for FAS)

### Option A: WordPress migration (recommended for FAS)
The existing fasmedicalsummitrcm.com is on WordPress. FAS already has a WP team. See `docs/WORDPRESS_DEPLOYMENT.md` for the migration approach. **Cost: $3-8K via dev agency, ~2-3 weeks.**

### Option B: Static deploy (faster, cheaper, requires DNS change)
Deploy the existing 24 HTML files directly:
- **Netlify** (drag-and-drop, free tier covers FAS volume)
- **Cloudflare Pages** (similar, free)
- **Vercel** (similar, free)
- Point fasmedicalsummitrcm.com DNS at the host
- Wire up forms via Formspree/Basin

**Cost: ~$0/month, 1-2 days work.** Tradeoff: FAS team won't be able to edit content via WordPress admin — they'd have to ask a dev to change copy.

### Option C: Hybrid
Keep the existing WordPress site for the blog/CMS section, deploy this site at the root. Trickier DNS configuration. Don't recommend unless there's a strong content team reason.
