# Markdown Management Directory

This directory contains all markdown-related files for site management and content creation.

## 📁 Directory Structure

```
site-helpers/md/
├── menu.md                    # Navigation menu structure
├── site.md                    # Sitemap page listing
├── MD-TO-HTML.md             # Markdown system guide
├── MARKDOWN-WORKFLOW.md      # How markdown processing works
├── html-to-md-templates.js   # Template generator script
├── md-new/                   # New markdown content (processed by build)
│   └── [your-new-pages.md]   # Create pages here
└── md-bak/                   # Reference templates (NOT processed)
    ├── README.md
    └── [template-files.md]   # Copy to md-new/ to use
```

## 🎯 Quick Start

### 1. Edit Site Navigation

**File:** `menu.md`

Edit this file to change the navigation menu structure.

```bash
# After editing:
cd ../../site-mng
node menu-builder.js
```

### 2. Edit Sitemap

**File:** `site.md`

Edit this file to manage which pages appear in the sitemap.

```bash
# After editing:
cd ../../site-mng
node sitemap-builder.js
```

### 3. Create New Page

**Location:** `md-new/`

1. Create a new .md file in `md-new/`:
```markdown
---
title: My New Page
path: folder/page.html
---

# Page Content

Write your content here in Markdown!
```

2. Build the site:
```bash
cd ../../site-mng
node md-to-html.js --all
```

3. Result: `HTML/folder/page.html` is created with full navigation!

### 4. Use Template

**Location:** `md-bak/`

Templates are reference copies of existing pages in markdown format.

To use a template:
```bash
# Copy template to md-new/
cp md-bak/software/software.md md-new/software.md

# Edit the file
nano md-new/software.md

# Build
cd ../../site-mng
node md-to-html.js --all
```

## 📝 File Purposes

| File | Purpose | Edit? |
|------|---------|-------|
| `menu.md` | Navigation structure | ✅ Edit often |
| `site.md` | Sitemap pages | ✅ Edit when adding pages |
| `md-new/*.md` | New page sources | ✅ Create/edit for pages |
| `md-bak/*.md` | Templates | 📋 Reference only |
| `MD-TO-HTML.md` | Documentation | 📖 Read for help |
| `MARKDOWN-WORKFLOW.md` | Documentation | 📖 Read for help |
| `html-to-md-templates.js` | Generator script | 🔧 Run to update templates |

## 🔄 Workflow

### Adding a New Page (Markdown Method)

1. **Create** markdown in `md-new/mypage.md`
2. **Add frontmatter** with title and path
3. **Write content** in markdown
4. **Build site**: `cd ../../site-mng && build-site.bat`
5. **Add to menu** in `menu.md` (optional)
6. **Add to sitemap** in `site.md` (optional)
7. **Rebuild**: `cd ../../site-mng && build-site.bat`

### Editing Navigation

1. **Edit** `menu.md`
2. **Build**: `cd ../../site-mng && node menu-builder.js`
3. **Check** your site - navigation updates instantly!

### Editing Sitemap

1. **Edit** `site.md`
2. **Build**: `cd ../../site-mng && node sitemap-builder.js`
3. **Check** `../sitemap.xml` and `../site-map.html`

## 🚫 What NOT to Do

❌ **Don't edit files in `md-bak/`** - These are templates only
❌ **Don't create pages in `md/` root** - Use `md-new/` subdirectory
❌ **Don't manually edit generated files** (site-nav.js, sitemap.xml, etc.)

## 💡 Tips

**New page workflow:**
- Simple content → Use markdown (`md-new/`)
- Complex layout → Use HTML template (`../../site-mng/template.html`)

**Template usage:**
- Browse `md-bak/` for examples
- Copy any to `md-new/` to activate
- Modify as needed

**Path handling:**
- Frontmatter `path:` is relative to `HTML/` directory
- `path: folder/page.html` → creates `HTML/folder/page.html`
- Links in content adjust automatically!

## 🔗 Related Files

- **Build scripts**: `../../site-mng/`
- **Generated output**: `../site-nav.js`, `../footer-loader.js`, etc.
- **HTML output**: `../../HTML/`
- **Dependencies**: `../package.json`, `../node_modules/`

## 📚 Documentation

**For detailed information:**
- `MD-TO-HTML.md` - Complete markdown system guide
- `MARKDOWN-WORKFLOW.md` - Processing behavior
- `../../site-mng/SITE-MANAGEMENT.md` - Overall site management
- `../../site-mng/QUICK-REF.md` - Quick reference card

## ⚙️ Installation

**First time setup:**
```bash
cd ..
npm install marked
```

This installs the markdown parser needed by `md-to-html.js`.

---

## Example: Creating Your First Page

```bash
# 1. Create file
echo "---
title: My First Markdown Page
path: blog/first-post.html
---

# Hello World!

This is my **first** markdown page.

## Features

- Easy to write
- Auto navigation
- Theme support

[Back to home](../index.html)
" > md-new/first-post.md

# 2. Build
cd ../../site-mng
node md-to-html.js --all

# 3. Check output
# Open: ../../HTML/blog/first-post.html
```

---

**All markdown management happens here!**
*Keep this directory organized and your site builds will be effortless.*
