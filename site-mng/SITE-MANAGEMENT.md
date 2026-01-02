# tiMaxal Hub - Site Management

This document explains how to maintain the site navigation and sitemap without coding knowledge.

## 📋 Overview

The site uses simple Markdown (`.md`) files that you can edit with any text editor. After editing, run simple Node.js scripts to update the site files.

## 🗂️ File Structure

**Site Management (site-mng/):**
- **menu.md** - Define the site navigation menu
- **menu-builder.js** - Script to generate site-nav.js and footer-loader.js from menu.md
- **site.md** - Define all pages for the sitemap
- **sitemap-builder.js** - Script to generate sitemap.xml and site-map.html from site.md
- **template.html** - Template for new pages
- **build-site.bat** - Runs both builder scripts

**Content Structure:**
- **HTML/** - All content pages go here (or in subdirectories)
  - HTML/aboutlife/, HTML/software/, HTML/sellhns/, HTML/varhns/
  - Up to 3 levels deep: HTML/varhns/FishingHowTo/page.html
- **site-helpers/** - Navigation, footer, theme scripts (auto-loaded by pages)

## 🔧 How to Update the Navigation Menu

### 1. Edit menu.md

Open `menu.md` in any text editor and make your changes:

```markdown
## Main Sites

- [Page Name](./HTML/folder/page.html)
  Optional description text
```

**Important:** All content page paths must start with `./HTML/`

**Format Rules:**
- `## Section Name` creates a category header
- `- [Text](path)` creates a menu link
- Add `{external}` for external links: `- [Text](https://url.com) {external}`
- Indent with 2 spaces for sub-items: `  - [Sub Item](path)`
- Add description on the next line (no dash, but prefix with spaces)

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
1. Create page in HTML/ directory (e.g., HTML/software/newpage.html)
2. Open `menu.md`
3. Add line: `- [New Page](./HTML/software/newpage.html)`
4. Run: `node menu-builder.js`

**Add new page to sitemap:**
1. Open `site.md`
2. Add line: `- [New Page](./HTML/software/newpage.html) | 0.7 | monthly`
3. Run: `node sitemap-builder.js`

**Update both at once:**
```powershell
node menu-builder.js; node sitemap-builder.js
```

### Example menu.md Entry

```markdown
## Content Pages

- [Photography](./HTML/varhns/fotografi/fotografi.html)
  Browse our photo collection
  - [CC-BY Images](./HTML/varhns/fotografi/cc-by_img.html)
  - [CC0 Images](./HTML/varhns/fotografi/cc0img.html)
```

### Example site.md Entry

```markdown
### Photography Section
- [Photography](./HTML/varhns/fotografi/fotografi.html) | 0.8 | weekly
- [CC-BY Images](./HTML/varhns/fotografi/cc-by_img.html) | 0.7 | monthly
- [CC0 Images](./HTML/varhns/fotografi/cc0img.html) | 0.7 | monthly
```

## ❓ Troubleshooting

**Menu not updating?**
- Make sure you ran `node menu-builder.js`
- Clear browser cache (Ctrl+F5)
- Check console for errors (F12)

**Links not working?**
- Content pages must use `./HTML/` prefix: `./HTML/folder/page.html`
- Use `./` prefix only: no `/HTML/` (without dot)
- External links need full URL: `https://example.com`
- Add `{external}` for external links in menu.md
- Check your script references match depth (../, ../../, or ../../../)

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
