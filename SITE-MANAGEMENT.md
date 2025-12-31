# tiMaxal Hub - Site Management

This document explains how to maintain the site navigation and sitemap without coding knowledge.

## 📋 Overview

The site uses simple Markdown (`.md`) files that you can edit with any text editor. After editing, run simple Node.js scripts to update the site files.

## 🗂️ File Structure

- **menu.md** - Define the site navigation menu
- **menu-builder.js** - Script to generate site-nav.js from menu.md
- **site.md** - Define all pages for the sitemap
- **sitemap-builder.js** - Script to generate sitemap.xml and site-map.html from site.md

## 🔧 How to Update the Navigation Menu

### 1. Edit menu.md

Open `menu.md` in any text editor and make your changes:

```markdown
## Main Sites

- [Page Name](./folder/page.html)
  Optional description text
```

**Format Rules:**
- `## Section Name` creates a category header
- `- [Text](path)` creates a menu link
- Add `{external}` for external links: `- [Text](https://url.com) {external}`
- Indent with 2 spaces for sub-items: `  - [Sub Item](path)`
- Add description on the next line (no dash)

### 2. Run the Builder Script

Open PowerShell/Terminal in the site folder and run:

```powershell
node menu-builder.js
```

This regenerates `site-nav.js` with your changes.

### 3. Test Your Changes

Open any page in a browser - the menu will be updated automatically!

## 🗺️ How to Update the Sitemap

### 1. Edit site.md

Open `site.md` in any text editor:

```markdown
- [Page Title](./path/to/page.html) | 0.8 | weekly
```

**Format Rules:**
- Each page on one line
- Format: `- [Title](path) | priority | changefreq`
- Priority: 0.0 to 1.0 (1.0 = most important)
- Change Frequency: daily, weekly, monthly, yearly
- Use `### Section Name` to organize pages

### 2. Run the Builder Script

```powershell
node sitemap-builder.js
```

This generates:
- `sitemap.xml` - For search engines (SEO)
- `site-map.html` - Human-readable site map page

### 3. Submit to Search Engines

After generating sitemap.xml, submit it to search engines:
- Google: https://search.google.com/search-console
- Bing: https://www.bing.com/webmasters

## 📝 Quick Reference

### Common Tasks

**Add a new page to menu:**
1. Open `menu.md`
2. Add line: `- [New Page](./folder/page.html)`
3. Run: `node menu-builder.js`

**Add new page to sitemap:**
1. Open `site.md`
2. Add line: `- [New Page](./folder/page.html) | 0.7 | monthly`
3. Run: `node sitemap-builder.js`

**Update both at once:**
```powershell
node menu-builder.js; node sitemap-builder.js
```

### Example menu.md Entry

```markdown
## Content Pages

- [Photography](./photos/gallery.html)
  Browse our photo collection
  - [Nature Photos](./photos/nature.html)
  - [City Photos](./photos/city.html)
```

### Example site.md Entry

```markdown
### Photography Section
- [Photo Gallery](./photos/gallery.html) | 0.8 | weekly
- [Nature Photos](./photos/nature.html) | 0.7 | monthly
- [City Photos](./photos/city.html) | 0.7 | monthly
```

## ❓ Troubleshooting

**Menu not updating?**
- Make sure you ran `node menu-builder.js`
- Clear browser cache (Ctrl+F5)
- Check console for errors (F12)

**Links not working?**
- Use `./` prefix for relative paths: `./folder/page.html`
- External links need full URL: `https://example.com`
- Add `{external}` for external links in menu.md

**Script errors?**
- Make sure Node.js is installed: `node --version`
- Check file paths are correct
- Look for syntax errors in .md files

## 🚀 Advanced Tips

**Reorder menu items:** Just move the lines in menu.md

**Remove a page:** Delete or comment out the line (add `#` at start)

**Change base URL:** Edit the `Base URL:` line in site.md

**Backup before changes:** Copy menu.md and site.md before major edits

## 📦 Requirements

- Node.js (already installed if scripts work)
- Text editor (Notepad, VS Code, etc.)
- Basic understanding of file paths

That's it! No HTML or JavaScript knowledge needed. 🎉
