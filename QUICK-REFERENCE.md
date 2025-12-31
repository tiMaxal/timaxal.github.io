# Quick Reference Card 📝

## 🚀 Quick Updates

### Add a New Page
1. Copy `template.html` and rename it
2. Edit the content (look for ✏️ comments)
3. Adjust file paths if in a subfolder (. or .. or ../..)
4. Add to `menu.md` (if it should appear in navigation)
5. Add to `site.md` (to include in sitemap)
6. Run: `build-site.bat` (or both builder scripts)

### Update Menu
1. Open `menu.md`
2. Edit the text
3. Run: `node menu-builder.js`
   (This rebuilds both site-nav.js AND footer-loader.js)

### Update Sitemap  
1. Open `site.md`
2. Edit the text
3. Run: `node sitemap-builder.js`

### Update Both
Double-click: `build-site.bat`
OR run: `node menu-builder.js; node sitemap-builder.js`

---

## 📄 Menu Format (menu.md)

```markdown
## Section Name

- [Link Text](./path/to/page.html)
  Optional description

- [External Link](https://url.com) {external}
  
  - [Sub Item](./path.html)
    (use 2 spaces for indent)

### Sub-Section Name
(Creates a nested group within a section)

- [Link](./path.html)
  Description
```

---

## 🗺️ Sitemap Format (site.md)

```markdown
### Section Name
- [Page Title](./path/to/page.html) | 0.8 | weekly

Priority: 0.0-1.0 (higher = more important)
Frequency: daily, weekly, monthly, yearly
```

---

## 🔍 File Paths

**Correct:**
- `./folder/page.html` ✅
- `./folder/subfolder/page.html` ✅

**Wrong:**
- `/folder/page.html` ❌ (missing dot)
- `folder/page.html` ❌ (missing ./)
- `E:/folder/page.html` ❌ (absolute path)

---

## 📂 Don't Edit These Files

These are auto-generated:
- `site-nav.js` (from menu.md)
- `footer-loader.js` (from menu.md)
- `sitemap.xml` (from site.md)
- `site-map.html` (from site.md)

---

## ✏️ DO Edit These Files

Source files:
- `menu.md` → controls navigation menu
- `site.md` → controls sitemap

---

## 🆘 Help

See full documentation: `SITE-MANAGEMENT.md`
See what was fixed: `FIXES-SUMMARY.md`

---

**Last Updated:** December 31, 2025
