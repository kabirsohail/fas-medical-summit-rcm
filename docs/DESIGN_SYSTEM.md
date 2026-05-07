# Design System

The complete visual language for the FAS Medical Summit site. Don't invent new colors, fonts, or spacing values — use these tokens.

## Palette

### Backgrounds (dark navy)

```css
--bg-deep:     #0A1220   /* Page background */
--bg-surface:  #0F1A2E   /* Raised surface (slightly lifted) */
--bg-elevated: #15233D   /* Cards, panels (most lifted) */
--bg-glass:    rgba(10, 18, 32, 0.7)   /* Glassmorphism for nav-scrolled */
```

### Accent (warm gold)

```css
--gold:        #C9A961   /* Primary accent — borders, eyebrows, CTAs */
--gold-bright: #E5C97D   /* Hover state, highlight, gradient end */
--gold-deep:   #8F6D2F   /* Gradient start, depth */
```

### Text (cream + grays)

```css
--ink-primary:   #F4EFE6   /* Body text, headings on dark bg */
--ink-secondary: #B8B0A0   /* Muted body text, descriptions */
--ink-tertiary:  #7A8090   /* Labels, metadata, eyebrows */
```

### Status

```css
--crimson: #B85450   /* Alerts, declining trends, errors */
--emerald: #4A7C6F   /* Success, positive trends, online indicators */
```

### Lines / dividers

```css
--line:        rgba(244, 239, 230, 0.08)   /* Default borders */
--line-strong: rgba(244, 239, 230, 0.14)   /* Emphasized borders */
```

## Typography

### Font families

```css
--serif: 'Fraunces', Georgia, 'Times New Roman', serif
--sans:  'Plus Jakarta Sans', -apple-system, system-ui, sans-serif
--mono:  'JetBrains Mono', 'SF Mono', Consolas, monospace
```

Loaded from Google Fonts in every page's `<head>`.

### Scale

| Element | Font | Size | Weight | Letter-spacing |
|---|---|---|---|---|
| Hero h1 | Fraunces | clamp(48px, 6vw, 88px) | 300 | -0.03em |
| Section h2 | Fraunces | clamp(36px, 4vw, 52px) | 300 | -0.025em |
| Card h3 | Fraunces | 22-28px | 400 | -0.015em |
| Body | Plus Jakarta Sans | 15-17px | 400 | 0 |
| Eyebrow | JetBrains Mono | 11-12px | 600 | 0.16em |
| Label | JetBrains Mono | 10-11px | 500 | 0.12em |
| Stats numbers | Fraunces (italic) | 32-72px | 400-500 | -0.02em |

### Italic-serif highlight

`<span class="serif-italic">` is used for emphasis in section headings — e.g., "End-to-end revenue cycle. *One unified partner.*" The italic word is colored gold.

## Spacing scale

```
4   8   12   16   24   32   48   64   80   120   160
```

Use only these values. No 7px, no 23px.

## Border-radius

```css
--radius-sm: 8px    /* Inputs, badges, small chips */
--radius-md: 14px   /* Medium cards */
--radius-lg: 18px   /* Large cards, sections, hero panels */
--radius-pill: 100px   /* Buttons, pill badges */
--radius-circle: 50%   /* Round buttons, dot indicators */
```

## Shadows

```css
/* Subtle elevation (default cards) */
0 12px 32px rgba(0, 0, 0, 0.25)

/* Lifted (hover state) */
0 24px 60px rgba(0, 0, 0, 0.35)

/* With gold glow (premium hover) */
0 24px 60px rgba(0, 0, 0, 0.35), 0 0 80px -20px rgba(201, 169, 97, 0.4)

/* Inner highlight (top edge of cards) */
inset 0 1px 0 rgba(255, 255, 255, 0.06)
```

## Easing

```css
--ease-out:    cubic-bezier(0.16, 1, 0.3, 1)        /* Default — smooth, decelerating */
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)    /* Springy — for hover lifts, button presses */
```

## Layout

- **Container max-width:** 1320px
- **Container side padding:** 32px (desktop), 22px (mobile)
- **Section vertical padding:** 120-160px desktop, 80px mobile
- **Grid gaps:** 18-32px

## Breakpoints

```css
@media (max-width: 1024px) { /* Tablet */ }
@media (max-width: 920px)  { /* Tablet (some elements) */ }
@media (max-width: 640px)  { /* Phone */ }
```

## Components

### Buttons

```html
<a href="..." class="btn btn-primary">Free Consultation →</a>
<a href="..." class="btn btn-ghost">Learn more →</a>
<a href="..." class="nav-cta">Free Consultation →</a>
```

### Eyebrow label

```html
<span class="eyebrow">Operational Scale</span>
```

Renders as small uppercase mono text in gold. Use above section h2s.

### Reveal-on-scroll

```html
<div class="reveal">...</div>
<div class="reveal reveal-delay-1">...</div>
<div class="reveal reveal-delay-2">...</div>
```

Element fades up from 30px below as it enters the viewport. Delays stagger reveals.

### 3D card with mouse-tilt

```html
<a class="service-card" data-tilt>
  <div class="service-card-bg"></div>
  <div class="service-card-glow"></div>
  <div class="service-card-shine"></div>
  <!-- content -->
</a>
```

Powered by the tilt JS at the bottom of `index.html`. Disabled on touch / mobile / reduced-motion.

### Floating dashboard mockup card

Used in why-us and platform sections.

```html
<div class="why-3d-card layer-front">
  <div class="why-3d-card-head">
    <span class="dot dot-red"></span>
    <span class="dot dot-yellow"></span>
    <span class="dot dot-green"></span>
    <span class="why-3d-card-title">METRIC_NAME</span>
    <span class="why-3d-live">EXAMPLE</span>
  </div>
  <!-- chart / content -->
</div>
```

The `EXAMPLE` tag is critical — never use `LIVE` unless the data is genuinely real-time.

## Animation patterns

| Pattern | Duration | Easing |
|---|---|---|
| Fade up reveal | 800ms | ease-out |
| Card hover lift | 400ms | ease-out |
| Button press | 200ms | ease-spring |
| Tilt tracking | 16ms (rAF) | linear |
| Glow drift | 8-20s | ease-in-out infinite |
| Card float (idle) | 6s | ease-in-out infinite |
| Pulse dot | 2s | ease-in-out infinite |
| Shine sweep on hover | 700ms | ease-out |
| Bar fill on view | 1.4s | ease-spring |

All animations must have a `prefers-reduced-motion: reduce` fallback.

## Accessibility tokens

- All decorative SVGs have `aria-hidden="true"`
- All interactive icons have `aria-label="..."`
- Focus rings are gold (`outline: 2px solid var(--gold)`) — never removed
- Minimum touch target: 44×44 px on mobile
- Minimum contrast ratio: 4.5:1 for body text against bg
