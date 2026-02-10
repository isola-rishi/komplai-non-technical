# Figma Integration Guide for Komplai Collaterals

**Purpose:** Connect your Figma design system to the collateral creation workflow
**Last Updated:** February 3, 2026

---

## Overview

This guide explains how to use Figma alongside Claude to create consistently-styled web artifacts, presentations, documents, and other collaterals that match your brand identity.

---

## Architecture: How Figma Fits In

```
┌─────────────────┐
│  Figma File     │  ← Your source of truth for designs
│  (Design System)│
└────────┬────────┘
         │
         ├─── Variables (colors, spacing, typography)
         ├─── Components (buttons, cards, layouts)
         └─── Design tokens

         ↓

┌─────────────────┐
│  Claude         │  ← Extracts design tokens and creates artifacts
│  (Collateral    │
│   Generator)    │
└────────┬────────┘
         │
         ├─── HTML/React artifacts
         ├─── PPTX presentations
         ├─── DOCX documents
         └─── XLSX spreadsheets

         ↓

┌─────────────────┐
│  Your Brand-    │  ← Consistently styled outputs
│  Consistent     │
│  Collaterals    │
└─────────────────┘
```

---

## Setup: Three Approaches

### Approach 1: Design-First (Recommended for Complex Projects)

**Best for:** Complex applications, design-heavy collaterals, or when you have existing Figma files

**Workflow:**
1. Design your screens/layouts in Figma
2. Share the Figma URL with Claude
3. Claude extracts the design context and generates code that matches your designs
4. Claude can reference specific Figma components and apply their styling

**Steps:**
1. Open your Figma file
2. Select the frame/component you want to implement
3. Copy the Figma URL (it should include `node-id=`)
4. Share with Claude: "Implement this Figma design: [URL]"

**Example:**
```
User: "Create a landing page based on this Figma design:
https://figma.com/design/abc123/MyFile?node-id=1-2"

Claude: [Uses get_design_context to extract the design]
        [Creates HTML/React artifact matching the Figma design]
```

### Approach 2: Tokens-First (Current Setup)

**Best for:** Quick collaterals, consistent styling across different artifact types

**Workflow:**
1. Claude extracts design tokens from your live website (already done!)
2. Claude applies these tokens to all artifacts you create
3. You can update tokens in Figma and re-sync as needed

**What we've created for you:**
- ✅ `komplai-design-system.md` - Complete design documentation
- ✅ `komplai-design-system.css` - Ready-to-use CSS file
- ✅ `komplai-react-example.jsx` - React component library

**To use:**
```
User: "Create a landing page for our new product launch"

Claude: [Imports komplai-design-system.css]
        [Creates HTML artifact using Komplai colors, fonts, and spacing]
        [Result: Brand-consistent landing page]
```

### Approach 3: Hybrid (Best of Both Worlds)

**Best for:** Teams with established design systems who need flexibility

**Workflow:**
1. Maintain design tokens in Figma Variables
2. Use Claude to extract and apply tokens automatically
3. For specific layouts, reference Figma designs directly
4. For quick iterations, use the token system

---

## Using Figma Tools with Claude

### Available Figma Capabilities

Claude has access to several Figma integration tools:

1. **`get_design_context`** - Extract complete design information from a Figma node
   - Colors, typography, spacing, layout
   - Generates code that matches the design
   - Returns asset download URLs

2. **`get_screenshot`** - Capture visual representation of a Figma frame
   - Useful for visual reference
   - Can be used to verify design implementation

3. **`get_variable_defs`** - Extract Figma variables
   - Color variables
   - Spacing variables
   - Typography variables
   - Can sync these to your CSS custom properties

4. **`get_code_connect_map`** - Map Figma components to code components
   - Links design and implementation
   - Ensures consistency between design and code

### Example Workflows

#### Workflow 1: Creating a Landing Page from Figma

```
You: "Create a landing page based on this Figma design:
https://figma.com/design/fileKey123/KomplaiLanding?node-id=1-234"

Claude will:
1. Extract the design using get_design_context
2. Identify colors, fonts, spacing, images
3. Generate HTML/React code matching the design exactly
4. Provide download links for any images/assets
5. Apply Komplai brand styling consistently
```

#### Workflow 2: Updating Design Tokens

```
You: "Update the design system with the latest variables from Figma:
https://figma.com/design/fileKey123/KomplaiDesignSystem?node-id=0-1"

Claude will:
1. Extract variables using get_variable_defs
2. Update komplai-design-system.css with new values
3. Provide a summary of what changed
4. You can then regenerate any artifacts with updated styling
```

#### Workflow 3: Creating Presentation with Figma Assets

```
You: "Create a pitch deck using the slide templates from Figma:
https://figma.com/design/fileKey123/SlideTemplates"

Claude will:
1. Extract slide layouts from Figma
2. Export any graphics/images
3. Create a PPTX file matching the Figma designs
4. Apply Komplai color scheme and typography
```

---

## Best Practices

### 1. Organize Your Figma Files

**Recommended Structure:**
```
Komplai Design System (File)
├── 📄 Cover & Overview
├── 🎨 Colors & Variables
├── 📝 Typography
├── 🧩 Components
│   ├── Buttons
│   ├── Cards
│   ├── Forms
│   └── Navigation
├── 📐 Layouts
│   ├── Landing Pages
│   ├── Dashboard
│   └── Marketing Pages
└── 📊 Templates
    ├── Slide Decks
    ├── One-Pagers
    └── Reports
```

### 2. Use Figma Variables

Create variables for:
- **Colors:** Primary, secondary, accent, neutrals
- **Spacing:** 4px, 8px, 12px, 16px, 24px, 32px, etc.
- **Typography:** Font sizes, line heights, weights
- **Border Radius:** Corner radius values

**Benefit:** When Claude extracts variables, your entire design system updates automatically.

### 3. Name Your Frames Descriptively

Good names help Claude understand what to implement:
- ✅ "Hero Section - Dark Background"
- ✅ "Product Card - With CTA"
- ✅ "Dashboard - Status Overview"
- ❌ "Frame 123"
- ❌ "Copy of Copy of Layout"

### 4. Use Components and Auto Layout

- **Components:** Reusable elements (buttons, cards)
- **Auto Layout:** Ensures spacing is consistent
- **Variants:** Different states of the same component

When Claude extracts these, it creates more maintainable code.

### 5. Keep a "Reference" Page

Create a page with:
- Color swatches with names
- Typography examples
- Spacing examples
- Component gallery
- Example layouts

Share this page's URL with Claude for quick reference.

---

## Common Workflows

### Creating a New Landing Page

**Step 1:** Design in Figma (or use existing design)
**Step 2:** Share Figma URL with Claude
**Step 3:** Claude generates HTML/React artifact
**Step 4:** Preview and iterate

**Prompt Template:**
```
"Create a landing page based on this Figma design: [URL]

Focus on:
- [Section 1 description]
- [Section 2 description]
- [Any specific requirements]

Use the Komplai design system for colors and typography."
```

### Creating a Pitch Deck

**Step 1:** Define content and structure
**Step 2:** Reference Figma slide templates (if available)
**Step 3:** Claude creates PPTX with Komplai styling

**Prompt Template:**
```
"Create a pitch deck with the following slides:
1. [Slide title and content]
2. [Slide title and content]
...

Use the Komplai design system:
- Dark green backgrounds for key slides
- Playfair Display for headlines
- Include the status dashboard design from our website
[Optional: Reference specific Figma slides: URL]"
```

### Creating Marketing Materials

**Step 1:** Define the material (one-pager, brochure, etc.)
**Step 2:** Specify Figma assets to use
**Step 3:** Claude generates DOCX/PDF with Komplai branding

**Prompt Template:**
```
"Create a one-pager about [topic]:
- Use Komplai brand colors and typography
- Include hero section with dark green background
- [Specific content requirements]
[Optional: Use images from Figma: URL]"
```

---

## Maintaining Consistency

### When to Update Design Tokens

Update your design tokens when:
- Brand colors change
- Typography is updated
- New components are added
- Spacing system evolves

### How to Update

1. Update your Figma file
2. Share the updated URL with Claude
3. Claude extracts new tokens
4. Regenerate affected collaterals

### Version Control

Consider versioning your design system:
```
komplai-design-system-v1.0.css
komplai-design-system-v1.1.css
komplai-design-system-v2.0.css
```

This lets you maintain older collaterals while updating new ones.

---

## Troubleshooting

### "Claude can't access my Figma file"

**Solution:** Ensure your Figma file is set to "Anyone with the link can view"

1. Open your Figma file
2. Click "Share" in the top-right
3. Set to "Anyone with the link"
4. Copy the share link

### "The colors don't match exactly"

**Solution:** Extract colors directly from Figma variables

```
You: "Get the exact color values from this Figma file:
[URL to your design system page]"

Claude will extract precise RGB/hex values.
```

### "The fonts look different"

**Solution:** Ensure fonts are loaded

For web artifacts, Claude needs to import fonts:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

Claude handles this automatically, but verify the fonts are available.

### "Layout doesn't match the Figma design"

**Solution:** Share the specific frame URL

Instead of the file URL, share the frame URL:
1. Select the frame in Figma
2. Copy link to selection (right-click → Copy/Paste → Copy link to selection)
3. Share this URL with Claude

---

## Advanced: Code Connect Integration

If you're using Figma's Code Connect feature, Claude can:

1. Map Figma components to your existing code components
2. Generate code that references your component library
3. Maintain consistency between design and implementation

**Example:**
```
You: "Map this Figma button to our Button component:
[Figma URL with button selected]

Our Button component is in src/components/Button.tsx"

Claude will create a Code Connect mapping file.
```

---

## Quick Reference Card

| Task | Figma Input | Claude Output |
|------|-------------|---------------|
| Landing page | Figma design URL | HTML/React artifact |
| Pitch deck | Slide template URLs | PPTX file |
| Design tokens | Variables page URL | Updated CSS file |
| Marketing doc | Layout + assets | DOCX/PDF file |
| Dashboard | Dashboard design | React component |
| Update branding | New colors in Figma | Updated design system |

---

## Next Steps

1. **Organize Your Figma Files:** Create or update your design system file
2. **Set Up Variables:** Define colors, spacing, typography in Figma
3. **Create Templates:** Design templates for common collateral types
4. **Test Integration:** Try creating a simple landing page from Figma
5. **Iterate:** Refine your design system based on what works

---

## Resources

- **Komplai Design System:** [komplai-design-system.md](./komplai-design-system.md)
- **CSS Implementation:** [komplai-design-system.css](./komplai-design-system.css)
- **React Examples:** [komplai-react-example.jsx](./komplai-react-example.jsx)
- **Figma Documentation:** [figma.com/developers](https://www.figma.com/developers)
- **Code Connect:** [figma.com/developers/code-connect](https://www.figma.com/developers/code-connect)

---

## Questions?

If you need help with:
- Extracting specific design elements from Figma
- Creating a particular type of collateral
- Updating the design system
- Troubleshooting integration issues

Just ask! Share your Figma URL and describe what you're trying to create.
