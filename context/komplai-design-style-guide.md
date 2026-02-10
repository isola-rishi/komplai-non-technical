# KOMPLAI
## Design & Style Guide

**Version 2.0 | February 2026**

*Audit-ready finance automation for your business*

---

## 📋 What's New in Version 2.0

This version updates all design tokens to match the live website at miraculous-discussions-935540.framer.app. Key changes:

- **Colors:** Updated to darker, richer green palette (from #0A1F1C to rgb(2, 31, 14))
- **Typography:** Headlines now use Playfair Display (serif) instead of Instrument Sans
- **Accent colors:** Brighter green indicators (rgb(69, 209, 99)) and warm yellow alerts
- **Enhanced component patterns:** Added status badges, progress bars, and alert cards based on actual product UI

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

### Design Philosophy

Komplai's visual design reflects trust, sophistication, and clarity for financial automation. The aesthetic combines:
- **Dark, rich greens** that evoke stability, growth, and financial security
- **Elegant serif typography** for headlines that convey authority and timelessness
- **Clean, modern interfaces** with generous spacing and clear data presentation
- **Subtle depth** through layered green tones rather than heavy shadows
- **Data-forward visualization** with clear status indicators and actionable insights

---

## 2. Color Palette

### Primary Colors

The Komplai color system is built around a deep, sophisticated green palette that conveys professionalism, trust, and financial stability. The dark theme creates focus and reduces visual fatigue for finance professionals who spend long hours reviewing data.

| Color Name | RGB Value | Hex | Usage |
|------------|-----------|-----|-------|
| **Deep Forest** | rgb(2, 31, 14) | `#021F0E` | Primary background, headers, hero sections |
| **Forest Green** | rgb(22, 84, 46) | `#16542E` | Buttons, primary actions, CTAs |
| **Hunter Green** | rgb(56, 102, 66) | `#386642` | Secondary buttons, card backgrounds |
| **True Black** | rgb(0, 0, 0) | `#000000` | Text, accents, strong emphasis |
| **Pure White** | rgb(255, 255, 255) | `#FFFFFF` | Text on dark backgrounds, cards |

### Accent Colors

| Color Name | RGB Value | Hex | Usage |
|------------|-----------|-----|-------|
| **Bright Green** | rgb(69, 209, 99) | `#45D163` | Success indicators, completed states, growth metrics |
| **Muted Green** | rgb(58, 99, 81) | `#3A6351` | Muted backgrounds, secondary card elements |
| **Sage Green** | rgb(45, 87, 54) | `#2D5736` | Tertiary elements, subtle accents |
| **Warm Yellow** | rgb(255, 238, 189) | `#FFEEBD` | Callouts, warning states, "pending" badges |

### Neutral Colors

| Color Name | RGB Value | Hex | Usage |
|------------|-----------|-----|-------|
| **Off-White** | rgb(247, 247, 247) | `#F7F7F7` | Light section backgrounds |
| **Light Gray** | rgb(235, 235, 235) | `#EBEBEB` | Borders, dividers |
| **Medium Gray** | rgb(102, 102, 102) | `#666666` | Secondary text, muted elements |
| **Dark Gray** | rgb(47, 44, 37) | `#2F2C25` | Primary text on light backgrounds |
| **Charcoal** | rgb(34, 34, 34) | `#222222` | Heading text on light backgrounds |
| **Brown Gray** | rgb(74, 72, 71) | `#4A4847` | Tertiary text |

### Semantic Colors

Use these semantic color mappings for consistent UI states:

| Semantic Use | Color Value | When to Use |
|--------------|-------------|-------------|
| **Success / Complete** | rgb(69, 209, 99) | Completed tasks, verified items, positive metrics |
| **Warning / Pending** | rgb(255, 238, 189) | Pending items, items needing attention |
| **Risk / Alert** | rgb(255, 238, 189) with orange text | Risk alerts, critical items |
| **Growth / Positive** | rgb(69, 209, 99) | Positive growth metrics, ahead-of-schedule items |
| **Progress Active** | rgb(255, 165, 0) | In-progress tasks (orange) |
| **Progress Inactive** | rgb(102, 102, 102) | Not started tasks |

### Opacity Variants

For overlays, subtle backgrounds, and layered effects:

```css
--white-95: rgba(255, 255, 255, 0.95);     /* Semi-transparent overlays */
--white-60: rgba(255, 255, 255, 0.6);      /* Muted text on dark */
--white-40: rgba(255, 255, 255, 0.4);      /* Borders on dark */
--white-20: rgba(255, 255, 255, 0.2);      /* Subtle borders */
--white-18: rgba(255, 255, 255, 0.18);     /* Very subtle backgrounds */
--charcoal-70: rgba(34, 34, 34, 0.7);      /* Subtle text */
--charcoal-40: rgba(34, 34, 34, 0.4);      /* Muted elements */
--charcoal-10: rgba(34, 34, 34, 0.1);      /* Very light borders */
```

### Color Usage Guidelines

1. **Maintain 70-20-10 ratio:** 70% deep forest/dark backgrounds, 20% white (text/cards), 10% accent colors (highlights/CTAs)
2. **Contrast requirements:** All text must meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
3. **Green hierarchy:** Use darker greens for backgrounds, mid-tone greens for interactive elements, bright green for success/completion states
4. **Never use:** Pure bright green (#00FF00), bright neon colors, or colors that compete with the primary palette

---

## 3. Typography

### Font Families

The Komplai type system combines elegant serif headlines with clean, readable sans-serif body text to create a sophisticated yet approachable aesthetic.

#### Primary Display: Playfair Display (Serif)
Used for headlines, hero text, and major section headers. A classical serif font that conveys authority, sophistication, and timelessness—perfect for communicating trust in financial applications.

**Font Weight:** Bold (700)
**Fallbacks:** serif
**Import:** `@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');`

#### Body: Inter (Sans-Serif)
Used for body text, UI elements, and longer-form content. Optimized for screen readability with excellent x-height and open letterforms.

**Font Weights:** Regular (400), Medium (500), Semibold (600)
**Fallbacks:** system-ui, sans-serif
**Import:** `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');`

#### Alternative Sans-Serif Options
For specific UI contexts, these alternatives are available:
- **Inter Display:** UI labels, buttons, badges
- **Reddit Sans:** Alternative body text
- **Geist:** Alternative UI text

#### Monospace: JetBrains Mono (Optional)
Used for code snippets, technical data, and financial figures where character alignment matters.

**Fallbacks:** Fira Code, monospace

### Type Scale

| Style | Font | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|------|--------|-------------|----------------|-------|
| **Hero** | Playfair Display | 72px | Bold (700) | 1.1 | -0.02em | Landing page heroes, major announcements |
| **H1** | Playfair Display | 56px | Bold (700) | 1.2 | -0.01em | Page titles, major section headers |
| **H2** | Playfair Display | 36px | Bold (700) | 1.2 | 0 | Section headers, feature titles |
| **H3** | Playfair Display | 28px | Bold (700) | 1.25 | 0 | Card titles, subsection headers |
| **Subheading** | Inter | 20px | Regular (400) | 1.6 | 0 | Intro paragraphs, subheadings |
| **Body Large** | Inter | 18px | Regular (400) | 1.6 | 0 | Lead text, important body copy |
| **Body** | Inter | 16px | Regular (400) | 1.6 | 0 | General body copy, descriptions |
| **Body Small** | Inter | 14px | Regular (400) | 1.5 | 0 | Secondary information |
| **UI Label** | Inter Display | 14px | Medium (500) | 1.4 | 0 | Labels, button text |
| **Caption** | Inter | 13px | Regular (400) | 1.5 | 0 | Helper text, metadata |
| **Badge** | Inter Display | 12px | Semibold (600) | 1.3 | 0.5px | Badges, tags (uppercase) |

### Typography Guidelines

- **Headlines:** Use sentence case for most headers; use title case sparingly for brand materials
- **Serif for impact:** Use Playfair Display for any text that needs authority or emphasis
- **Line length:** Optimal 60-75 characters (approximately 900px max-width) for body text
- **Paragraph spacing:** 1.5x the body font size between paragraphs (typically 24px)
- **Hierarchy:** Maintain clear visual hierarchy—large serif headlines → medium sans-serif subheads → readable body text

---

## 4. Visual Elements & Imagery

### Design Language

Komplai's visual language is characterized by clean lines, generous whitespace, and a dark-mode-first aesthetic that feels modern and professional. The design should evoke precision, reliability, and intelligent automation.

**Key Visual Principles:**
- **Depth through color, not shadow:** Use layered green tones rather than heavy shadows
- **Data-forward:** Prioritize clear presentation of financial data and status
- **Purposeful whitespace:** Let content breathe; avoid visual clutter
- **Rounded corners:** Soften the technical nature with approachable rounded elements
- **Subtle animations:** Use gentle transitions to guide attention without distraction

### Imagery Guidelines

- **Product Screenshots:** Show clean, realistic dashboard interfaces with actual data visualizations. Avoid stock-looking interfaces.
- **Abstract Graphics:** Use geometric patterns, flowing lines, and data visualization elements that suggest connectivity and automation.
- **Photography:** When used, favor authentic images of modern workspaces and diverse finance professionals. Avoid cliché corporate imagery.
- **Icons:** Use line-style icons with consistent 2px stroke weight. Prefer rounded corners for a friendlier feel.
- **Illustrations:** Minimal, functional illustrations that support understanding—not decorative.

### Spacing System

Use an 8px base grid for all spacing to maintain consistent rhythm throughout the interface.

| Token | Value | Usage |
|-------|-------|-------|
| **xs** | 8px | Tight spacing, icon gaps, small element padding |
| **sm** | 12px | Component internal spacing |
| **md** | 16px | Component padding, comfortable element gaps |
| **lg** | 24px | Card padding, related element spacing |
| **xl** | 32px | Section element spacing |
| **2xl** | 48px | Section gaps, major spacing breaks |
| **3xl** | 64px | Large section padding |
| **4xl** | 96px | Hero section padding, major page sections |

**Section padding:** Typically 64-96px vertical padding for major sections.

### Border Radius

Rounded corners soften the technical nature of financial software and create a more approachable aesthetic.

| Element Type | Radius Value | Usage |
|-------------|--------------|-------|
| **Small elements** | 6px | Small buttons, tight UI elements |
| **Standard UI** | 8px | Buttons, input fields, standard components |
| **Cards** | 10-16px | Card containers, feature boxes |
| **Large cards** | 16-24px | Hero cards, major content blocks |
| **Pills** | 40px | Badges, tags, pill-shaped buttons |

### Shadows & Depth

Use subtle shadows for depth. On dark backgrounds, rely more on border treatments and color layering than shadows.

**Minimal shadow (light backgrounds):**
```css
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
            0 2px 4px -1px rgba(0, 0, 0, 0.06);
```

**Elevated shadow (hover states):**
```css
box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

**Dark background borders (instead of shadows):**
```css
border: 1px solid rgba(255, 255, 255, 0.1);
```

---

## 5. UI Components

### Buttons

#### Primary Button
- **Background:** rgb(22, 84, 46) on dark backgrounds; white on light backgrounds
- **Text:** White on dark buttons; rgb(2, 31, 14) on light buttons
- **Padding:** 12px 24px
- **Border-radius:** 8px
- **Font:** Inter Display, 16px, Medium (500)
- **Hover:** Background shifts to rgb(56, 102, 66)
- **Example:** "Get Started Now"

```css
.btn-primary {
  background: rgb(22, 84, 46);
  color: rgb(255, 255, 255);
  padding: 12px 24px;
  border-radius: 8px;
  font-family: 'Inter Display', sans-serif;
  font-size: 16px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}
.btn-primary:hover {
  background: rgb(56, 102, 66);
}
```

#### Secondary Button
- **Background:** Transparent
- **Border:** 1px solid rgba(255, 255, 255, 0.4) on dark; rgba(34, 34, 34, 0.2) on light
- **Padding:** 12px 24px
- **Border-radius:** 8px
- **Hover:** Subtle background fill with border color at 10-20% opacity
- **Example:** "Explore More"

```css
.btn-secondary {
  background: transparent;
  color: rgb(255, 255, 255);
  border: 1px solid rgba(255, 255, 255, 0.4);
  padding: 12px 24px;
  border-radius: 8px;
  font-family: 'Inter Display', sans-serif;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.6);
}
```

#### Text/Link Button
- **Color:** Inherit from context or use bright green rgb(69, 209, 99) for emphasis
- **No background or border**
- **Hover:** Underline
- **Example:** "Learn more →" links

### Cards

#### Feature Card (Dark Background)
- **Background:** rgb(58, 99, 81)
- **Border:** Optional 1px solid rgba(255, 255, 255, 0.1)
- **Border-radius:** 16px
- **Padding:** 32px
- **Text color:** White
- **Structure:** Icon/indicator → Title (Playfair Display, 24-28px) → Description (Inter, 16px) → Optional link

#### Feature Card (Light Background)
- **Background:** White
- **Border:** 1px solid rgb(235, 235, 235)
- **Border-radius:** 16px
- **Padding:** 32px
- **Text color:** rgb(34, 34, 34)
- **Hover:** Subtle lift with shadow

#### Alert Cards
Three types matching the product interface:

**Risk Alert:**
```css
.alert-risk {
  background: rgba(255, 100, 100, 0.1);
  border: 1px solid rgba(255, 100, 100, 0.3);
  color: rgb(255, 100, 100);
  padding: 16px;
  border-radius: 10px;
}
```

**Growth Alert:**
```css
.alert-growth {
  background: rgba(69, 209, 99, 0.1);
  border: 1px solid rgba(69, 209, 99, 0.3);
  color: rgb(69, 209, 99);
  padding: 16px;
  border-radius: 10px;
}
```

**Observation:**
```css
.alert-observation {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgb(255, 255, 255);
  padding: 16px;
  border-radius: 10px;
}
```

### Status Badges

Small, uppercase labels that indicate status:

```css
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 40px;
  font-family: 'Inter Display', sans-serif;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-pending {
  background: rgb(255, 238, 189);
  color: rgb(133, 77, 14);
}

.badge-complete {
  background: rgb(69, 209, 99);
  color: rgb(2, 31, 14);
}

.badge-risk {
  background: rgba(255, 100, 100, 0.2);
  color: rgb(200, 50, 50);
}
```

### Progress Bars

Used extensively in the dashboard to show task completion:

```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: rgb(235, 235, 235);
  border-radius: 40px;
  overflow: hidden;
}

.progress-fill-complete {
  background: rgb(69, 209, 99);  /* Green for completed */
}

.progress-fill-partial {
  background: rgb(255, 165, 0);  /* Orange for in-progress */
}

.progress-fill-inactive {
  background: rgb(102, 102, 102);  /* Gray for not started */
}
```

### Task List Items

A key component in the Komplai interface:

```css
.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgb(58, 99, 81);
  border-radius: 10px;
  color: white;
  transition: background 0.2s ease;
}

.task-item:hover {
  background: rgb(45, 87, 54);
}
```

**Structure:** Status indicator (circle with icon) → Task title → Avatar → Progress count

### Avatar/Initials

Circular avatars with initials:

```css
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgb(34, 34, 34);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter Display', sans-serif;
  font-size: 14px;
  font-weight: 600;
  border: 2px solid rgba(255, 255, 255, 0.2);
}
```

### Navigation

- **Header:** Fixed position, deep forest background rgb(2, 31, 14), white text
- **Height:** 72-80px
- **Nav items:** Inter, 16px, Medium weight, subtle hover states
- **Logo:** Komplai wordmark in white, approximately 120px wide
- **CTA Button:** Primary button style in the navigation

---

## 6. Voice & Tone

### Brand Voice Principles

1. **Confident, not arrogant:** We know our product works. We don't need to oversell.
2. **Clear, not simplistic:** Finance professionals are smart. Respect their intelligence while making complex concepts accessible.
3. **Helpful, not pushy:** Focus on outcomes and benefits. "Your team that closes your books while you sleep" not "Buy now!"
4. **Modern, not trendy:** Avoid buzzwords that will date quickly. "AI-powered" is acceptable; "Web3 synergy" is not.
5. **Data-driven:** Use specific metrics and concrete examples. "65% faster" beats "much faster."

### Headline Style

- **Lead with outcomes:** *"Audit-ready finance automation for your business"*
- **Use action-oriented language:** *"Close books faster, prevent errors, reclaim time"*
- **Personify the product when appropriate:** *"Your team that closes your books while you sleep"*
- **Be specific:** *"Close your books 65% faster"* not *"Save time"*
- **Use sentence case:** Capitalize only the first word and proper nouns

### Body Copy Style

- **Short sentences. Direct statements.** Break up complex ideas into digestible chunks.
- **Use second person** ("your books", "your team") to make it personal
- **Concrete specifics over vague claims:** *"Queues that used to take days now take minutes"*
- **Three-part rhythm for impact:** *"no clutter, no noise, no bottlenecks"*
- **Show, don't just tell:** Demonstrate value with examples and data
- **Respect the reader's time:** Get to the point quickly

### Larry (AI Agent) Voice

When writing as or about Larry, maintain a helpful, capable, slightly personified tone. Larry is a competent assistant, not a robot or a human pretending to be helpful.

**Tone:** Professional, capable, supportive
**Not:** Overly cute, overly robotic, trying to be human

**Examples:**
- ✅ "Larry handles bookkeeping, AR and AP, reporting, and insights"
- ✅ "Larry ensures accurate entries, timely filings, and traceable records"
- ✅ "Larry delivers actionable insights across finance and operations"
- ❌ "Larry is so excited to help you today!"
- ❌ "SYSTEM: Processing financial data..."
- ❌ "Larry thinks you should..."

### Words to Use

| Instead of... | Use... |
|---------------|--------|
| Leverage | Use |
| Utilize | Use |
| Solution | Platform / Tool / System |
| Synergy | (avoid entirely) |
| Cutting-edge | Modern / Intelligent / Advanced |
| Revolutionary | (show results instead of claiming it) |
| Disruptive | (show impact instead) |
| Game-changing | (demonstrate with data) |

### Words That Work

Strong, clear words that resonate with finance professionals:

- Audit-ready
- Continuous close
- Real-time
- Automated / Automates
- Visibility / Transparent
- Insights / Actionable
- Traceable / Trackable
- Compliant / Compliance
- Accurate / Precision
- Efficient / Efficiency
- Streamlined
- Reconciliation
- Exception-based
- Validated

### Tone by Context

**Website/Marketing:** Confident, clear, outcome-focused
**Product UI:** Helpful, direct, informative
**Documentation:** Clear, thorough, patient
**Error Messages:** Honest, helpful, actionable
**Success Messages:** Affirming without being excessive

---

## 7. Application Examples

### Website Sections

#### Hero Section
- **Background:** Deep forest rgb(2, 31, 14)
- **Layout:** Centered content with generous vertical padding (96px+)
- **Headline:** Playfair Display, 72px, bold, white
- **Subheadline:** Inter, 18px, white with 90% opacity, max-width 900px
- **CTAs:** Two buttons—primary "Get Started Now" and secondary "Explore More"
- **Visual element:** Product screenshot or abstract graphic below
- **Optional:** Small indicator with dot and text above headline ("Welcome to Komplai")

**Example structure:**
```
[Small indicator with green dot] Welcome to Komplai

Audit-ready finance automation
for your business.

Komplai handles the tedious 90% of bookkeeping, reconciliation,
and reporting through its finance agent - Larry. Close your books
65% faster, eliminate manual errors, and reclaim your team's time
for high-level strategy.

[Get Started Now]  [Explore More →]

[Product screenshot or visualization]
```

#### Feature Grid
- **Section header:** Playfair Display, 56px, centered
- **Subtext:** Inter, 18px, centered, max-width 900px
- **Grid:** 2x2 or 3x3 grid of feature cards with consistent spacing (24px gaps)
- **Each card:**
  - Icon or status indicator
  - Title (Playfair Display, 24-28px)
  - Description (Inter, 16px)
  - Optional "Learn more →" link
- **Background:** Can alternate between dark forest and light off-white sections

#### Dashboard Showcase
- **Background:** Dark forest rgb(2, 31, 14) to show off the actual product
- **Structure:**
  - Section title and description
  - Large dashboard screenshot or interactive demo
  - Key metrics or features highlighted with callouts
  - Status cards showing "Current Close Status" with task list
  - Alert cards (Risk, Growth, Observation)

#### Pricing Section (if applicable)
- **Clear hierarchy between tiers:** Launch vs Pro vs Enterprise
- **Tier name:** Prominently displayed
- **Brief, scannable descriptions:** Bullet points or short paragraphs
- **Single CTA per tier**
- **Visual distinction:** Use borders, backgrounds, or elevation to differentiate tiers

### Marketing Materials

#### Pitch Decks
- **Slide backgrounds:** Deep forest rgb(2, 31, 14) or black for dark slides; white for data-heavy slides
- **Headlines:** Playfair Display, 48-64px, white or charcoal depending on background
- **Body text:** Inter, 16-18px
- **Accent color:** Bright green rgb(69, 209, 99) for emphasis and data visualization
- **One key message per slide:** Don't overcrowd
- **Data visualizations:** Use green palette (muted to bright) for charts and graphs
- **Generous padding:** Minimum 80px on all sides

**Slide types:**
- **Title slide:** Logo + tagline + visual element
- **Problem slide:** Dark background, clear statement of the pain point
- **Solution slide:** Product screenshot with key features highlighted
- **How it works:** Simple 3-step diagram or process flow
- **Impact slide:** Large metric with context
- **Team slide:** Photos + brief bios on white background
- **CTA slide:** Clear next step with contact information

#### One-Pagers
- **Logo:** Prominently at top (left or center)
- **Headline:** Playfair Display, 36-40px, states the value prop clearly
- **Sections:**
  - Brief intro paragraph
  - 3-4 key features with icons and short descriptions
  - Social proof (testimonial, logo carousel, or key metric)
  - Clear CTA
  - Contact information footer
- **Design:** Can use white background with green accents, or dark green header with white body
- **Length:** Truly one page—no continued pages

#### Social Media / LinkedIn
- **Format:** Square (1:1) or 4:5 for feed posts
- **Bold headlines:** Playfair Display or Inter Bold, large enough to read on mobile
- **Background:** Deep forest with white text, or white with dark text
- **Product screenshots:** Use device frames when showing UI
- **Tone:** Professional but not corporate—conversational and data-driven
- **Always include:** Clear value statement or specific metric

**Post types:**
- **Feature announcement:** Screenshot + brief explanation + benefit
- **Customer story:** Metric + context + brief testimonial
- **Thought leadership:** Industry insight + Komplai perspective
- **Tips & best practices:** Actionable advice for finance teams

#### Email Templates
- **Subject lines:** Clear, specific, benefit-driven (8-10 words max)
- **Header:** Logo + clean navigation
- **Body:**
  - Personalized greeting
  - Single, clear message (don't try to say everything)
  - Visual element (screenshot, diagram, or illustration)
  - Clear CTA button
  - Brief P.S. or additional value if needed
- **Footer:** Standard contact info, unsubscribe, social links
- **Design:** Simple, clean, mobile-friendly
- **Colors:** Use green sparingly for CTAs and accents on white background

---

## 8. Appendix: CSS Variables Reference

Use these CSS custom properties for consistent implementation across all Komplai properties:

```css
:root {
  /* ==========================================
     COLORS - PRIMARY
     ========================================== */
  --color-primary-dark: rgb(2, 31, 14);       /* #021F0E - Main background */
  --color-primary: rgb(22, 84, 46);           /* #16542E - Buttons, CTAs */
  --color-primary-alt: rgb(56, 102, 66);      /* #386642 - Secondary actions */
  --color-black: rgb(0, 0, 0);                /* #000000 - True black */
  --color-white: rgb(255, 255, 255);          /* #FFFFFF - Pure white */

  /* ==========================================
     COLORS - ACCENT
     ========================================== */
  --color-accent-bright: rgb(69, 209, 99);    /* #45D163 - Success, growth */
  --color-accent-muted: rgb(58, 99, 81);      /* #3A6351 - Card backgrounds */
  --color-accent-sage: rgb(45, 87, 54);       /* #2D5736 - Tertiary elements */
  --color-accent-yellow: rgb(255, 238, 189);  /* #FFEEBD - Warnings, callouts */

  /* ==========================================
     COLORS - NEUTRAL
     ========================================== */
  --color-gray-50: rgb(247, 247, 247);        /* #F7F7F7 - Light backgrounds */
  --color-gray-100: rgb(235, 235, 235);       /* #EBEBEB - Borders */
  --color-gray-400: rgb(102, 102, 102);       /* #666666 - Secondary text */
  --color-gray-600: rgb(74, 72, 71);          /* #4A4847 - Tertiary text */
  --color-gray-800: rgb(47, 44, 37);          /* #2F2C25 - Primary dark text */
  --color-gray-900: rgb(34, 34, 34);          /* #222222 - Headings */

  /* ==========================================
     COLORS - SEMANTIC
     ========================================== */
  --color-success: var(--color-accent-bright);
  --color-warning: var(--color-accent-yellow);
  --color-growth: var(--color-accent-bright);
  --color-risk: var(--color-accent-yellow);

  /* ==========================================
     COLORS - OPACITY VARIANTS
     ========================================== */
  --color-white-95: rgba(255, 255, 255, 0.95);
  --color-white-60: rgba(255, 255, 255, 0.6);
  --color-white-40: rgba(255, 255, 255, 0.4);
  --color-white-20: rgba(255, 255, 255, 0.2);
  --color-white-18: rgba(255, 255, 255, 0.18);
  --color-charcoal-70: rgba(34, 34, 34, 0.7);
  --color-charcoal-40: rgba(34, 34, 34, 0.4);
  --color-charcoal-10: rgba(34, 34, 34, 0.1);

  /* ==========================================
     TYPOGRAPHY - FONTS
     ========================================== */
  --font-display: 'Playfair Display', serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-ui: 'Inter Display', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* ==========================================
     TYPOGRAPHY - SIZES
     ========================================== */
  --text-hero: 72px;
  --text-h1: 56px;
  --text-h2: 36px;
  --text-h3: 28px;
  --text-h4: 20px;
  --text-body-lg: 18px;
  --text-body: 16px;
  --text-body-sm: 14px;
  --text-caption: 13px;
  --text-badge: 12px;

  /* ==========================================
     SPACING
     ========================================== */
  --spacing-xs: 8px;
  --spacing-sm: 12px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;
  --spacing-4xl: 96px;

  /* ==========================================
     BORDER RADIUS
     ========================================== */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --radius-xl: 16px;
  --radius-2xl: 24px;
  --radius-pill: 40px;

  /* ==========================================
     SHADOWS
     ========================================== */
  --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
               0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
               0 10px 10px -5px rgba(0, 0, 0, 0.04);

  /* ==========================================
     TRANSITIONS
     ========================================== */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

### Quick Reference Table

| Element | Background | Text Color | Font | Size |
|---------|-----------|------------|------|------|
| Hero | rgb(2, 31, 14) | White | Playfair Display | 72px |
| H1 | Inherit | Inherit | Playfair Display | 56px |
| H2 | Inherit | Inherit | Playfair Display | 36px |
| Body | Inherit | White/Charcoal | Inter | 16px |
| Button Primary | rgb(22, 84, 46) | White | Inter Display | 16px |
| Button Secondary | Transparent | Inherit | Inter Display | 16px |
| Card Dark | rgb(58, 99, 81) | White | Inter | 16px |
| Card Light | White | rgb(34, 34, 34) | Inter | 16px |
| Badge Success | rgb(69, 209, 99) | rgb(2, 31, 14) | Inter Display | 12px |
| Badge Pending | rgb(255, 238, 189) | rgb(133, 77, 14) | Inter Display | 12px |

---

## Implementation Checklist

Use this checklist when creating any Komplai materials:

### Visual Design
- [ ] Use Playfair Display (serif) for all headlines (H1, H2, H3)
- [ ] Use Inter for body text and UI elements
- [ ] Apply primary dark green rgb(2, 31, 14) for hero/main sections
- [ ] Use appropriate border radius (6-8px for UI, 10-24px for cards)
- [ ] Implement status colors consistently (bright green = success, yellow = warning)
- [ ] Use 8px base spacing grid
- [ ] Ensure proper contrast ratios (WCAG AA minimum)
- [ ] Test responsive behavior at 320px, 768px, 1024px, and 1440px breakpoints

### Content & Copy
- [ ] Lead with outcomes and benefits, not features
- [ ] Use specific data and metrics where possible
- [ ] Write in second person ("your team", "your books")
- [ ] Keep sentences short and direct
- [ ] Use sentence case for headlines
- [ ] Avoid buzzwords and jargon
- [ ] Ensure Larry's voice is helpful and capable, not cutesy

### Brand Consistency
- [ ] Logo properly sized and positioned
- [ ] Tagline used correctly: "Audit-ready finance automation for your business"
- [ ] Brand personality evident (professional, intelligent, clean, empowering)
- [ ] Tone appropriate for context (confident but not arrogant)

---

## Resources & Tools

### Fonts
- **Playfair Display:** [Google Fonts](https://fonts.google.com/specimen/Playfair+Display)
- **Inter:** [Google Fonts](https://fonts.google.com/specimen/Inter) or [rsms.me/inter](https://rsms.me/inter/)
- **JetBrains Mono:** [jetbrains.com/mono](https://www.jetbrains.com/lp/mono/)

### Color Tools
- **Contrast Checker:** [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- **Palette Generator:** [Coolors.co](https://coolors.co/)

### Design Assets
- **Logo files:** Available in the Komplai brand assets folder
- **Product screenshots:** Request from product team for latest UI
- **Icon library:** Use line-style icons with 2px stroke weight

### Accessibility
- **WCAG Guidelines:** [w3.org/WAI/WCAG21/quickref/](https://www.w3.org/WAI/WCAG21/quickref/)
- **Minimum contrast ratios:**
  - Normal text: 4.5:1
  - Large text (18px+ or 14px+ bold): 3:1
  - UI components: 3:1

---

*This style guide is a living document. As Komplai evolves, these guidelines should be updated to reflect brand evolution while maintaining consistency with established foundations. Last updated: February 2026.*
