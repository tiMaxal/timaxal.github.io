# 🚀 Quick Reference Card

## Common Tasks

### Build Everything

```bash
cd site-mng
build-site.bat        # Windows
./build-site.sh       # Linux/Mac
```

Includes: helper path normalization + favicon normalization + menu + sitemap + markdown conversion.

### Edit Navigation Menu

```bash
1. Edit: site-helpers/md/menu.md
2. Run: cd site-mng && node menu-builder.js
3. Changes appear in navigation hover menu
```

### Add Page to Sitemap

```bash
1. Edit: site-helpers/md/site.md
2. Add: - [Page Title](./path/to/page.html) | 0.8 | weekly
3. Run: cd site-mng && node sitemap-builder.js
4. Updates: sitemap.xml + site-map.html
```

### Create New Page (Markdown)

```bash
1. Create: site-helpers/md/md-new/mypage.md
2. Add frontmatter:
   ---
   title: My Page
   path: mypage.html
   ---
3. Write content in Markdown
4. Run: cd site-mng && node md-to-html.js --all
5. Output: HTML/mypage.html
```

### Convert Existing Page

```bash
1. Copy: site-helpers/md/md-bak/page.md → site-helpers/md/md-new/
2. Edit: site-helpers/md/md-new/page.md
3. Run: cd site-mng && node md-to-html.js --all
4. Test: HTML/page.html (regenerated)
```

---

## File Locations

| What | Where | Edit? |
|------|-------|-------|
| Navigation structure | site-helpers/md/menu.md | ✅ Edit |
| Sitemap pages | site-helpers/md/site.md | ✅ Edit |
| Markdown sources (new) | site-helpers/md/md-new/ | ✅ Edit |
| Markdown templates | site-helpers/md/md-bak/ | 📋 Reference |
| Markdown docs | site-helpers/md/*.md | 📚 Docs |
| Generated navigation | site-helpers/site-nav.js | ❌ Auto |
| Footer template | site-helpers/footer.html | ✅ Edit |
| Hand-crafted HTML | HTML/*.html | ✅ Edit* |

*Unless matching .md file exists in site-helpers/md/md-new/

---

## Path Syntax in menu.md

```markdown
## Category Name

- [Link Text](HTML/folder/page.html)       # Internal page
- [External](https://example.com) {external}  # External site
  - [Sub Item](HTML/folder/sub.html)      # Indent = sub-item
```

**Important:**

- NO `./` prefix
- Paths relative to site root
- `HTML/` for pages in HTML folder
- `site-helpers/` for utility pages

---

## Markdown Frontmatter

```markdown
---
title: Page Title          # Required: Browser tab title
path: folder/page.html     # Optional: Output path (relative to HTML/)
---

# Your Content Here
```

If `path` omitted, outputs to `HTML/[filename].html`

---

## Decision Tree: HTML or Markdown?

```
New page needed?
├─ Simple content (text, links, images)
│  └─ Use MARKDOWN
│     ├─ Create: site-helpers/md/page.md
│     └─ Build: generates HTML/page.html
│
└─ Complex layout/features
   └─ Use HTML TEMPLATE
      ├─ Copy: site-mng/template.html
      └─ Edit: Save to HTML/page.html
```

---

## No-JS Users

**Navigation Options:**

1. ✅ **Footer Sitemap Link** (current)
   - Always visible
   - Link: `🗺️ Site Map`
   - Works without JS

2. 🔧 **Static Nav Bar** (optional)
   - Run: `node static-nav-builder.js`
   - Shows: Home | AboutLife | Software | etc.
   - Auto-hides when JS available

---

## Generated Files

**DO NOT EDIT THESE:**

- site-helpers/site-nav.js
- site-helpers/footer-loader.js  
- site-helpers/sitemap.xml
- site-helpers/site-map.html
- HTML files with matching .md in site-helpers/md/

**Regenerate with:** `build-site.bat` or individual scripts

---

## Troubleshooting

**Navigation links broken?**

- Check menu.md paths (no `./` prefix)
- Run: `node menu-builder.js`

**Page not in sitemap?**

- Add to site.md
- Run: `node sitemap-builder.js`

**Markdown not converting?**

- Check .md file in site-helpers/md/ (not md-bak/)
- Verify frontmatter syntax
- Run: `node md-to-html.js --all`

**HTML edits disappeared?**

- Check if .md file exists for that page
- Markdown overwrites HTML on build
- Solution: Edit .md file instead

**Path duplication (/HTML/HTML/)?**

- Check menu.md for `./` prefixes
- Should be: `HTML/page.html`
- Not: `./HTML/page.html`

---

## Build Order

When making multiple changes:

```bash
1. Edit menu.md and/or site.md
2. Create/edit .md files
3. Run: build-site.bat (does all at once)

OR individually:
1. node helper-paths-builder.js # Helper paths + favicon
2. node menu-builder.js         # Navigation
3. node sitemap-builder.js      # Sitemap
4. node md-to-html.js --all     # Markdown pages
```

---

## npm Scripts

```bash
cd site-mng

npm run build           # Everything
npm run build:helpers   # Helper paths + favicon only
npm run build:menu      # Navigation only
npm run build:sitemap   # Sitemap only
npm run build:pages     # Markdown only
```

---

## Template Directory (md-bak)

**Purpose:** Reference templates only

**Contains:** Converted versions of existing HTML pages

**Usage:**

```bash
# NOT processed by build
# Copy to md/ to activate:
cp site-helpers/md-bak/page.md site-helpers/md/
```

**Note:** Only 11 pages converted. Complex pages (donate.html, index.html, hns-pf.html) excluded.

---

## Performance

| Metric | Value |
|--------|-------|
| First page load | ~30 KB |
| Subsequent loads | ~5-15 KB |
| JS overhead | ~14 KB (cached) |
| No-JS fallback | ✅ Sitemap link |

See: `LOW-BANDWIDTH-OPTIONS.md` for optimization ideas

---

## Documentation

| Document | Topic |
|----------|-------|
| UPDATES-2026-01-24.md | Today's changes |
| MARKDOWN-WORKFLOW.md | How markdown processing works |
| MD-TO-HTML.md | Markdown system guide |
| LOW-BANDWIDTH-OPTIONS.md | Performance optimizations |
| SITE-MANAGEMENT.md | Overall site management |
| FIXES-SUMMARY.md | All fixes to date |

---

## Key Concepts

**Markdown = Source of Truth**

- Edit .md → HTML regenerated
- Never edit generated HTML

**menu.md ≠ site.md**

- menu.md = Navigation structure
- site.md = Sitemap pages
- Different purposes!

**md/ vs md-bak/**

- md/ = Processed by build
- md-bak/ = Reference only

**Paths**

- Relative to site root
- No `./` prefix
- `HTML/` for pages
- `site-helpers/` for utilities

---

*Keep this card handy for quick reference!*
