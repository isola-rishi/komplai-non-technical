# KOMPLAI
## Design & Style Guide

**Version 1.0 | January 2026**

*Audit-ready finance automation for your business*

---

## Contents

1. Brand Overview
2. Color Palette
3. Typography
4. Visual Elements & Imagery
5. UI Components
6. Voice & Tone
7. Application Examples
8. Appendix: CSS Variables Reference

---

## 1. Brand Overview

### Brand Positioning

Komplai is an AI-powered continuous close platform that positions itself as the intelligent execution layer for finance teams. The brand communicates sophistication, reliability, and cutting-edge technology while remaining approachable for finance professionals who may not be tech-native.

### Brand Personality

- **Professional & Trustworthy:** Finance teams need absolute confidence in their tools
- **Intelligent & Modern:** AI-native, not AI as an afterthought
- **Clean & Efficient:** No clutter, no noise, no bottlenecks
- **Empowering & Supportive:** "Your team that closes your books while you sleep"

### Core Value Proposition

**"Audit-ready finance automation for your business"** — This tagline encapsulates the promise: not just automation, but automation that produces audit-ready results. This distinction is critical for finance professionals who need compliance-grade outputs.

---

## 2. Color Palette

### Primary Colors

The Komplai color system is built around a deep, sophisticated green-black palette that conveys professionalism, trust, and modernity. The dark theme creates focus and reduces visual fatigue for finance professionals who spend long hours reviewing data.

| Color | Hex | Usage |
|-------|-----|-------|
| **Deep Forest** | `#0A1F1C` | Primary background, headers, hero sections |
| **True Black** | `#000000` | Text, accents, strong emphasis |
| **Pure White** | `#FFFFFF` | Text on dark backgrounds, cards |

### Accent Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Soft Mint** | `#C8E6C9` | Highlights, success states, feature cards |
| **Light Green** | `#E8F5E9` | Subtle backgrounds, hover states |
| **Teal Accent** | `#4DB6AC` | CTAs, buttons, interactive elements, links |

### Neutral Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Gray 100** | `#F5F5F5` | Light backgrounds |
| **Gray 200** | `#E0E0E0` | Borders |
| **Gray 400** | `#9E9E9E` | Muted text |
| **Gray 600** | `#616161` | Secondary text |
| **Gray 900** | `#212121` | Dark text on light backgrounds |

### Color Usage Guidelines

1. **Maintain 70-20-10 ratio:** 70% deep forest/black (backgrounds), 20% white (text/cards), 10% accent colors (highlights/CTAs)
2. **Contrast requirements:** All text must meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
3. **Never use:** Pure green (#00FF00), bright neon colors, or colors that compete with the primary palette

---

## 3. Typography

### Font Families

The Komplai type system uses clean, modern sans-serif fonts that communicate professionalism while maintaining excellent readability across devices.

#### Primary: Instrument Sans
Used for headlines, hero text, and display purposes. A geometric sans-serif with distinctive character that balances modernity with approachability.

**Fallbacks:** Inter, system-ui, sans-serif

#### Secondary: Inter
Used for body text, UI elements, and longer-form content. Optimized for screen readability with excellent x-height and open letterforms.

**Fallbacks:** system-ui, sans-serif

#### Monospace: JetBrains Mono
Used for code snippets, technical data, and financial figures where character alignment matters.

**Fallbacks:** Fira Code, monospace

### Type Scale

| Style | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Hero | 48-64px | Bold (700) | 1.0 | Landing page heroes, major announcements |
| H1 | 36-40px | Bold (700) | 1.1 | Page titles, major section headers |
| H2 | 28-32px | Semibold (600) | 1.2 | Section headers, feature titles |
| H3 | 20-24px | Semibold (600) | 1.25 | Card titles, subsection headers |
| H4 | 16-18px | Semibold (600) | 1.3 | Subheadings, labels |
| Body Large | 18px | Regular (400) | 1.5 | Intro paragraphs, lead text |
| Body | 16px | Regular (400) | 1.6 | General body copy, descriptions |
| Body Small | 14px | Regular (400) | 1.5 | Secondary information |
| Caption | 12-14px | Regular (400) | 1.4 | Labels, helper text, metadata |

### Typography Guidelines

- **Headlines:** Use sentence case, not title case
- **Line length:** Optimal 60-75 characters for body text
- **Letter spacing:** Slightly tighter (-0.01em) for large headlines; default for body
- **Paragraph spacing:** 1.5x the body font size between paragraphs

---

## 4. Visual Elements & Imagery

### Design Language

Komplai's visual language is characterized by clean lines, generous whitespace, and a dark-mode-first aesthetic that feels modern and professional. The design should evoke precision, reliability, and intelligent automation.

### Imagery Guidelines

- **Product Screenshots:** Show clean, realistic dashboard interfaces with actual data visualizations. Avoid stock-looking interfaces.
- **Abstract Graphics:** Use geometric patterns, flowing lines, and gradient meshes that suggest data flow and connectivity.
- **Photography:** When used, favor authentic images of modern workspaces and diverse finance professionals. Avoid cliché corporate imagery.
- **Icons:** Use line-style icons with consistent 2px stroke weight. Prefer rounded corners for a friendlier feel.

### Spacing System

Use an 8px base grid for all spacing.

| Token | Value | Usage |
|-------|-------|-------|
| xs | 8px | Tight spacing, icon gaps |
| sm | 16px | Component internal padding |
| md | 24px | Card padding, element gaps |
| lg | 32px | Section element spacing |
| xl | 48px | Section gaps |
| 2xl | 64px | Major section padding |
| 3xl | 96px | Hero section padding |

**Section padding:** Typically 80-120px vertical padding for major sections.

### Border Radius

| Element | Radius |
|---------|--------|
| Cards and containers | 12-16px |
| Buttons | 8px (slightly rounded, not pill-shaped) |
| Input fields | 8px |
| Small elements | 4px |

### Shadows & Depth

Use subtle shadows for depth. On dark backgrounds, rely more on border treatments than shadows.

**Primary shadow:**
```css
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
            0 2px 4px -1px rgba(0, 0, 0, 0.06);
```

**Elevated shadow:**
```css
box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

---

## 5. UI Components

### Buttons

#### Primary Button
- **Background:** White (#FFFFFF) on dark backgrounds, Deep Forest (#0A1F1C) on light backgrounds
- **Text:** Opposite of background
- **Padding:** 12px 24px
- **Border-radius:** 8px
- **Font:** 16px, Semibold
- **Hover:** Slight opacity reduction (0.9)
- **Example:** "Get Started Now"

#### Secondary Button
- **Background:** Transparent
- **Border:** 1px solid current text color
- **Padding:** 12px 24px
- **Border-radius:** 8px
- **Hover:** Subtle background fill (10% opacity of text color)
- **Example:** "Explore More"

#### Text/Link Button
- **Color:** Teal Accent (#4DB6AC) or inherit from context
- **No background**
- **Hover:** Underline
- **Example:** "Explore" links on feature cards

### Cards

#### Feature Card
- **Background:** Dark green (#0A1F1C) or white depending on section
- **Border:** 1px solid rgba(255,255,255,0.1) on dark, subtle gray on light
- **Border-radius:** 16px
- **Padding:** 32px
- **Shadow:** Subtle or none
- **Structure:** Number indicator (large, muted) → Title (H3) → Description (Body) → Link

#### Pricing Card
- **Background:** Semi-transparent or solid depending on tier
- **Border-radius:** 16px
- **Padding:** 40px
- **Structure:** Tier name (H4, accent color) → Description → CTA button
- **Differentiation:** Use visual distinction between tiers (e.g., bordered vs filled cards)

### Navigation

- **Header:** Fixed position, dark background, logo left-aligned, nav items center or right
- **Height:** 72-80px
- **Nav items:** 16px, Medium weight, subtle hover states
- **Logo:** Wordmark in white, approximately 120px wide

### Section Numbers

Feature sections use large, semi-transparent numbers (01, 02, 03...) to create visual hierarchy and guide the user through content.

- **Size:** 48-64px
- **Color:** Muted/semi-transparent version of text color (e.g., 20% opacity)
- **Position:** Above or beside feature title

---

## 6. Voice & Tone

### Brand Voice Principles

1. **Confident, not arrogant:** We know our product works. We don't need to oversell.
2. **Clear, not simplistic:** Finance professionals are smart. Respect their intelligence while making complex concepts accessible.
3. **Helpful, not pushy:** Focus on outcomes and benefits. "Your team that closes your books while you sleep" not "Buy now!"
4. **Modern, not trendy:** Avoid buzzwords that will date quickly. "AI-powered" is acceptable; "Web3 synergy" is not.

### Headline Style

- Lead with outcomes: *"Audit-ready finance automation for your business"*
- Use action-oriented language: *"Close books faster, prevent errors"*
- Personify the product when appropriate: *"Your team that closes your books while you sleep"*

### Body Copy Style

- Short sentences. Direct statements.
- Use second person ("your books", "your team") to make it personal
- Concrete specifics over vague claims: *"Queues that used to take days now take minutes"*
- Three-part rhythm for impact: *"no clutter, no noise, no bottlenecks"*

### Larry (AI Agent) Voice

When writing as or about Larry, maintain a helpful, capable, slightly personified tone. Larry is a competent assistant, not a robot or a human pretending to be helpful.

**Examples:**
- "Larry handles bookkeeping, AR and AP, reporting, and insights"
- "Larry ensures accurate entries, timely filings, and traceable records"
- "Larry delivers actionable insights across finance and operations"

### Words to Use

| Instead of... | Use... |
|---------------|--------|
| Leverage | Use |
| Utilize | Use |
| Solution | Platform / Tool |
| Synergy | (avoid entirely) |
| Cutting-edge | Modern / Intelligent |
| Revolutionary | (show, don't tell) |

### Words That Work

- Audit-ready
- Continuous close
- Real-time
- Automated / Automates
- Visibility
- Insights
- Traceable
- Compliant

---

## 7. Application Examples

### Website Sections

#### Hero Section
- Dark background (#0A1F1C)
- Large hero headline (48-64px, bold)
- Subheadline with value proposition
- Two CTAs (primary: "Get Started Now", secondary: "Explore More")
- Product screenshot or abstract graphic below
- Logo carousel of integrations/partners at bottom

#### Feature Grid
- Section header with explanatory subtext
- 2x3 or 3x2 grid of feature cards
- Each card: number (01-06), title, description, "Explore" link
- Alternating card treatments or consistent dark theme

#### Pricing Section
- Clear hierarchy between tiers (Launch vs Pro)
- Tier name prominently displayed
- Brief, scannable descriptions
- Single CTA per tier
- Visual distinction between tiers (e.g., bordered vs filled cards)

### Marketing Materials

#### Pitch Decks
- Dark slide backgrounds (Deep Forest or Black)
- White text with Teal accents for emphasis
- One key message per slide
- Data visualizations in mint/teal color palette
- Generous padding and breathing room

#### One-Pagers
- Logo prominently at top
- Clear headline that states the value prop
- Three or fewer key features with brief descriptions
- Social proof (testimonial or metric)
- Single, clear CTA
- Contact information

#### Social Media / LinkedIn
- Square or 4:5 format for graphics
- Bold headlines that work without context
- Brand colors as background with contrasting text
- Product screenshots with device frames when showing UI
- Professional but not corporate tone

---

## 8. Appendix: CSS Variables Reference

Use these CSS custom properties for consistent implementation:

```css
:root {
  /* Colors - Primary */
  --color-primary: #0A1F1C;
  --color-primary-light: #1A3F3C;
  --color-black: #000000;
  --color-white: #FFFFFF;
  
  /* Colors - Accent */
  --color-accent: #4DB6AC;
  --color-accent-light: #C8E6C9;
  --color-accent-lighter: #E8F5E9;
  
  /* Colors - Neutral */
  --color-gray-100: #F5F5F5;
  --color-gray-200: #E0E0E0;
  --color-gray-400: #9E9E9E;
  --color-gray-600: #616161;
  --color-gray-900: #212121;
  
  /* Colors - Semantic */
  --color-background-dark: #0A1F1C;
  --color-background-light: #FFFFFF;
  --color-text-primary: #FFFFFF;
  --color-text-secondary: #9E9E9E;
  --color-text-dark: #212121;
  
  /* Typography */
  --font-display: 'Instrument Sans', Inter, system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Font Sizes */
  --text-hero: 64px;
  --text-h1: 40px;
  --text-h2: 32px;
  --text-h3: 24px;
  --text-h4: 18px;
  --text-body-lg: 18px;
  --text-body: 16px;
  --text-body-sm: 14px;
  --text-caption: 12px;
  
  /* Spacing */
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 32px;
  --spacing-xl: 48px;
  --spacing-2xl: 64px;
  --spacing-3xl: 96px;
  
  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  
  /* Shadows */
  --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
               0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 
               0 10px 10px -5px rgba(0, 0, 0, 0.04);
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

---

*This style guide is a living document. As Komplai evolves, these guidelines should be updated to reflect brand evolution while maintaining consistency with established foundations.*
