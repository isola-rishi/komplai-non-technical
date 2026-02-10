# Komplai Design System

**Generated from:** https://miraculous-discussions-935540.framer.app/
**Date:** February 3, 2026
**Purpose:** Design tokens and styling guidelines for web artifacts (HTML/React)

---

## Design Philosophy

Komplai's design reflects trust, sophistication, and clarity for financial automation. The aesthetic combines:
- **Dark, rich greens** that evoke stability and growth
- **Elegant serif typography** for headlines that convey authority
- **Clean, modern interfaces** with generous spacing
- **Subtle depth** through layered green tones rather than shadows
- **Data-forward visualization** with clear status indicators

---

## Color Palette

### Primary Colors

```css
--primary-dark-green: rgb(2, 31, 14);      /* Main background, hero sections */
--primary-green: rgb(22, 84, 46);          /* Buttons, primary actions */
--primary-green-alt: rgb(56, 102, 66);     /* Secondary buttons, cards */
```

### Accent Colors

```css
--accent-bright-green: rgb(69, 209, 99);   /* Indicators, success states, active items */
--accent-muted-green: rgb(58, 99, 81);     /* Muted backgrounds, secondary elements */
--accent-sage-green: rgb(45, 87, 54);      /* Tertiary elements */
--accent-yellow: rgb(255, 238, 189);       /* Callouts, warning states */
```

### Neutral Colors

```css
--neutral-white: rgb(255, 255, 255);       /* Text on dark, card backgrounds */
--neutral-off-white: rgb(247, 247, 247);   /* Light section backgrounds */
--neutral-light-gray: rgb(235, 235, 235);  /* Borders, dividers */
--neutral-gray: rgb(102, 102, 102);        /* Secondary text */
--neutral-dark: rgb(47, 44, 37);           /* Primary text on light backgrounds */
--neutral-charcoal: rgb(34, 34, 34);       /* Heading text on light */
--neutral-brown-gray: rgb(74, 72, 71);     /* Tertiary text */
```

### Opacity Variants

```css
--white-95: rgba(255, 255, 255, 0.95);     /* Semi-transparent overlays */
--white-60: rgba(255, 255, 255, 0.6);
--white-40: rgba(255, 255, 255, 0.4);
--white-20: rgba(255, 255, 255, 0.2);
--white-18: rgba(255, 255, 255, 0.18);
--charcoal-70: rgba(34, 34, 34, 0.7);      /* Subtle text */
--charcoal-40: rgba(34, 34, 34, 0.4);
--charcoal-10: rgba(34, 34, 34, 0.1);      /* Very light borders */
```

### Semantic Colors

```css
/* Status Indicators */
--status-success: rgb(69, 209, 99);        /* Completed, verified */
--status-warning: rgb(255, 238, 189);      /* Pending, needs attention */
--status-growth: rgb(69, 209, 99);         /* Positive metrics */
--status-risk: rgb(255, 238, 189);         /* Risk alerts (pair with orange text) */

/* Progress Bars */
--progress-complete: rgb(69, 209, 99);     /* Completed tasks */
--progress-partial: rgb(255, 165, 0);      /* In progress (orange) */
--progress-inactive: rgb(102, 102, 102);   /* Not started */
```

---

## Typography

### Font Families

```css
/* Display/Headlines - Serif */
--font-display: "Playfair Display", "Playfair Display Placeholder", serif;

/* Body/UI - Sans Serif */
--font-body: "Inter", "Inter Placeholder", sans-serif;
--font-ui: "Inter Display", "Inter Display Placeholder", sans-serif;
--font-alt-1: "Reddit Sans", "Reddit Sans Placeholder", sans-serif;
--font-alt-2: "Geist", "Geist Placeholder", sans-serif;
```

### Type Scale & Usage

```css
/* Hero Headlines (Playfair Display) */
.hero-headline {
  font-family: var(--font-display);
  font-size: 72px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

/* Section Headlines (Playfair Display) */
.section-headline {
  font-family: var(--font-display);
  font-size: 56px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.01em;
}

/* Subheadings (Inter) */
.subheading {
  font-family: var(--font-body);
  font-size: 20px;
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: 0;
}

/* Body Text (Inter) */
.body-text {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 400;
  line-height: 1.6;
}

/* UI Labels (Inter) */
.ui-label {
  font-family: var(--font-ui);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
}

/* Small Text (Inter) */
.small-text {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 400;
  line-height: 1.5;
}
```

---

## Spacing & Layout

### Spacing Scale

```css
--space-xs: 8px;
--space-sm: 12px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
--space-4xl: 96px;
```

### Border Radius

```css
--radius-sm: 6px;       /* Small elements, tight corners */
--radius-md: 8px;       /* Standard UI elements */
--radius-lg: 10px;      /* Cards, containers */
--radius-xl: 16px;      /* Large cards */
--radius-2xl: 24px;     /* Hero cards, featured elements */
--radius-pill: 40px;    /* Pills, tags, rounded buttons */
```

---

## Component Patterns

### Buttons

```css
/* Primary Button */
.btn-primary {
  background: var(--primary-green);
  color: var(--neutral-white);
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-family: var(--font-ui);
  font-size: 16px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-primary:hover {
  background: var(--primary-green-alt);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: var(--neutral-white);
  padding: 12px 24px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.3);
  font-family: var(--font-ui);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
}
```

### Cards

```css
/* Dark Card (on dark backgrounds) */
.card-dark {
  background: var(--accent-muted-green);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  color: var(--neutral-white);
}

/* Light Card (on light backgrounds) */
.card-light {
  background: var(--neutral-white);
  border: 1px solid var(--neutral-light-gray);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  color: var(--neutral-dark);
}

/* Alert Card */
.card-alert {
  background: rgba(255, 238, 189, 0.2);
  border: 1px solid var(--accent-yellow);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
}
```

### Status Badges

```css
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  font-family: var(--font-ui);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-pending {
  background: var(--accent-yellow);
  color: rgb(133, 77, 14);
}

.badge-complete {
  background: var(--accent-bright-green);
  color: var(--primary-dark-green);
}

.badge-risk {
  background: rgba(255, 100, 100, 0.2);
  color: rgb(200, 50, 50);
}
```

### Progress Bars

```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--neutral-light-gray);
  border-radius: var(--radius-pill);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: var(--radius-pill);
  transition: width 0.3s ease;
}

.progress-complete {
  background: var(--status-success);
}

.progress-partial {
  background: rgb(255, 165, 0);
}
```

### Avatar/Initials

```css
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--neutral-charcoal);
  color: var(--neutral-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-ui);
  font-size: 14px;
  font-weight: 600;
  border: 2px solid rgba(255, 255, 255, 0.2);
}
```

---

## Layout Sections

### Hero Section

```css
.hero {
  background: var(--primary-dark-green);
  padding: var(--space-4xl) var(--space-lg);
  text-align: center;
  color: var(--neutral-white);
}

.hero h1 {
  font-family: var(--font-display);
  font-size: 72px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: var(--space-lg);
}

.hero p {
  font-family: var(--font-body);
  font-size: 18px;
  line-height: 1.6;
  max-width: 900px;
  margin: 0 auto;
}
```

### Feature Section (Light)

```css
.section-light {
  background: var(--neutral-off-white);
  padding: var(--space-3xl) var(--space-lg);
  color: var(--neutral-dark);
}

.section-light h2 {
  font-family: var(--font-display);
  font-size: 56px;
  text-align: center;
  margin-bottom: var(--space-2xl);
  color: var(--neutral-charcoal);
}
```

### Feature Section (Green)

```css
.section-green {
  background: var(--primary-green-alt);
  padding: var(--space-3xl) var(--space-lg);
  color: var(--neutral-white);
}
```

---

## Figma Integration Guide

### Step 1: Create Figma Variables

1. Open your Figma file
2. Go to the local variables panel
3. Create a new collection called "Komplai Design System"
4. Add color variables matching the tokens above
5. Add number variables for spacing and radius values

### Step 2: Apply Variables to Components

Map your Figma components to use these variables:
- Buttons → Use primary/secondary color variables
- Cards → Use background and border radius variables
- Typography → Create text styles matching the type scale
- Spacing → Use spacing variables for auto-layout gaps

### Step 3: Export Design Tokens

You can use Figma plugins like:
- **Design Tokens** - Export variables as JSON
- **Style Dictionary** - Convert to CSS/JS
- **Figma Tokens** - Sync between Figma and code

### Step 4: Link with Code Connect

Use Figma's Code Connect to map your components:
```typescript
// Button.figma.tsx
figma.connect(Button, "figma-node-id", {
  props: {
    variant: figma.enum("Variant", {
      primary: "primary",
      secondary: "secondary"
    })
  }
})
```

---

## Implementation Checklist

For each web artifact you create:

- [ ] Import design system CSS or create CSS custom properties
- [ ] Use Playfair Display for all headlines (h1, h2)
- [ ] Use Inter for body text and UI elements
- [ ] Apply primary dark green for hero/main sections
- [ ] Use appropriate border radius (8px for UI, 16-24px for cards)
- [ ] Implement status colors for alerts and indicators
- [ ] Add progress bars with semantic colors
- [ ] Use consistent spacing scale (8px base)
- [ ] Ensure proper contrast ratios (white text on dark green, dark text on light backgrounds)
- [ ] Test responsive behavior at different viewport sizes

---

## Quick Reference: CSS Custom Properties

```css
:root {
  /* Colors */
  --primary-dark-green: rgb(2, 31, 14);
  --primary-green: rgb(22, 84, 46);
  --primary-green-alt: rgb(56, 102, 66);
  --accent-bright-green: rgb(69, 209, 99);
  --accent-yellow: rgb(255, 238, 189);
  --neutral-white: rgb(255, 255, 255);
  --neutral-off-white: rgb(247, 247, 247);
  --neutral-gray: rgb(102, 102, 102);
  --neutral-dark: rgb(47, 44, 37);
  --neutral-charcoal: rgb(34, 34, 34);

  /* Typography */
  --font-display: "Playfair Display", serif;
  --font-body: "Inter", sans-serif;

  /* Spacing */
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* Border Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --radius-xl: 16px;
  --radius-2xl: 24px;
  --radius-pill: 40px;
}
```

---

## Resources

- **Font Sources:**
  - Playfair Display: [Google Fonts](https://fonts.google.com/specimen/Playfair+Display)
  - Inter: [Google Fonts](https://fonts.google.com/specimen/Inter) or [rsms.me/inter](https://rsms.me/inter/)

- **Color Contrast Checker:**
  - White on rgb(2, 31, 14): ✓ WCAG AAA compliant
  - Dark text on rgb(247, 247, 247): ✓ WCAG AA compliant

- **Accessibility Notes:**
  - Maintain minimum 4.5:1 contrast ratio for body text
  - Use 3:1 for large text (18px+ or 14px+ bold)
  - Ensure interactive elements have clear focus states
  - Provide text alternatives for color-coded information
