# Markdown to HTML Build System

This system allows you to write pages in Markdown and automatically convert them to HTML with full site navigation, footer, and theme support.

## Quick Start

### 1. Create a Markdown File

Create a new `.md` file in `site-helpers/md/` (or any subdirectory within it):

```markdown
---
title: My New Page
path: mynewpage.html
---

# My New Page

This is my page content written in **Markdown**!

## Features

- Easy to write
- Automatic navigation
- Theme support
```

### 2. Frontmatter (Required)

Each markdown file must start with frontmatter:

```yaml
---
title: Page Title  # Required: Shows in browser tab
path: folder/page.html  # Optional: Output path relative to HTML/
---
```

- `title`: The page title (shows in browser tab and can be used in headings)
- `path`: Where to output the HTML file relative to the `HTML/` directory
  - If omitted, outputs to `HTML/[filename].html`
  - Examples: `example.html`, `software/newapp.html`, `aboutlife/story.html`

### 3. Build Your Site

**Windows:**
```batch
cd site-mng
build-site.bat
```

**Linux/Mac:**
```bash
cd site-mng
chmod +x build-site.sh  # First time only
./build-site.sh
```

**Or convert markdown only:**
```bash
cd site-mng
node md-to-html.js --all          # Convert all .md files
node md-to-html.js myfile.md      # Convert specific file
```

## Directory Structure

```
timax.al-githubio/
├── site-helpers/
│   └── md/                    # Put your .md files here
│       ├── example.md
│       ├── software/          # Organize in subdirectories
│       │   └── myapp.md
│       └── about/
│           └── bio.md
│
├── HTML/                      # HTML files generated here
│   ├── example.html
│   ├── software/
│   │   └── myapp.html
│   └── about/
│       └── bio.html
│
└── site-mng/
    ├── md-to-html.js         # Conversion script
    ├── build-site.bat        # Windows build script
    └── build-site.sh         # Linux/Mac build script
```

## Markdown Features

All standard Markdown syntax is supported:

### Headings
```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Text Formatting
```markdown
**bold text**
*italic text*
***bold and italic***
~~strikethrough~~
```

### Lists
```markdown
- Bullet point 1
- Bullet point 2
  - Nested bullet

1. Numbered item 1
2. Numbered item 2
```

### Links
```markdown
[Link text](https://example.com)
[Internal link](../other-page.html)
```

### Images
```markdown
![Alt text](images/photo.jpg)
```

### Code
````markdown
Inline `code` with backticks

```javascript
// Code block
function example() {
  console.log("Hello!");
}
```
````

### Blockquotes
```markdown
> This is a quote
> Spanning multiple lines
```

### Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
| Data 3   | Data 4   |
```

## Automatic Features

Every generated HTML page automatically includes:

✅ **Navigation menu** - Hover over the 🏠 Home button
✅ **Theme switcher** - Light/Dark/Black theme support
✅ **Responsive footer** - With proper relative paths
✅ **Mobile-friendly** - Responsive design
✅ **Consistent styling** - Matches your site theme

## Path Handling

The script automatically adjusts paths based on output location:

- **Root level** (`HTML/page.html`):
  - Links to: `site-helpers/`
  
- **One level deep** (`HTML/folder/page.html`):
  - Links to: `../site-helpers/`
  
- **Two levels deep** (`HTML/folder/subfolder/page.html`):
  - Links to: `../../site-helpers/`

This happens automatically - no manual adjustment needed!

## Examples

### Simple Page
```markdown
---
title: About Me
path: about.html
---

# About Me

Welcome to my page! I'm a web developer who loves creating simple, clean websites.

## Skills

- HTML/CSS
- JavaScript
- Markdown

[Contact me](mailto:me@example.com)
```

### Page in Subfolder
```markdown
---
title: My Software Project
path: software/myproject.html
---

# My Software Project

This is my latest creation!

## Download

- [Windows version](downloads/app-windows.zip)
- [Mac version](downloads/app-mac.zip)
- [Linux version](downloads/app-linux.tar.gz)
```

## Adding to Site Navigation

After creating a page, to add it to the site menu:

1. Edit `site-mng/menu.md` - Add your page link
2. Edit `site-mng/site.md` - Add to sitemap
3. Run `build-site.bat` or `build-site.sh`

See `SITE-MANAGEMENT.md` for more details on menu and sitemap configuration.

## Dependencies

The markdown converter requires Node.js and the `marked` package:

```bash
npm install marked
```

(This is already included if you have `package.json` set up)

## Troubleshooting

**"No markdown files found"**
- Make sure you created `.md` files in `site-helpers/md/`
- The directory is created automatically on first run with an example file

**"Module 'marked' not found"**
- Run: `npm install marked`

**"Template.html not found"**
- Make sure `template.html` exists in `site-mng/`

**Generated HTML doesn't show navigation**
- Check that `site-helpers/site-nav.js` exists
- Verify the script paths in generated HTML are correct
- Run `build-site.bat` to regenerate all components

**Styling looks wrong**
- Verify `site-helpers/site-nav.css` exists
- Check browser console for 404 errors
- Clear browser cache and reload

## Comparison: Markdown vs HTML Template

### Using Markdown (Recommended for new pages)
✅ Faster to write
✅ Cleaner, more readable source
✅ Focus on content, not markup
✅ Automatic formatting
✅ Version control friendly
❌ Less control over exact HTML structure

### Using HTML Template (For complex layouts)
✅ Full control over layout
✅ Can add custom styles inline
✅ Complex interactive elements
❌ More verbose
❌ Requires HTML knowledge
❌ More time-consuming

## Tips

1. **Preview locally**: Open generated HTML files in your browser to preview
2. **Organize by topic**: Use subdirectories in `md/` to organize content
3. **Keep it simple**: Markdown is best for text-heavy content
4. **Use HTML for complex pages**: For highly styled pages, use the HTML template instead
5. **Version control**: Commit both `.md` source and generated `.html` files

## Next Steps

- Create your first markdown file in `site-helpers/md/`
- Run the build script to generate HTML
- Add the page to `menu.md` and `site.md`
- Commit and push your changes!

---

For more information, see:
- `SITE-MANAGEMENT.md` - Overall site management guide
- `QUICK-REFERENCE.md` - Quick reference for common tasks
- `template.html` - HTML template for complex pages
