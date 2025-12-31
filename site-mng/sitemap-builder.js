#!/usr/bin/env node
/**
 * Sitemap Builder Script
 * Converts site.md to sitemap.xml and generates site-map.html
 * 
 * Usage: node sitemap-builder.js
 */

const fs = require('fs');
const path = require('path');

// File paths
const SITE_MD = path.join(__dirname, 'site.md');
const SITEMAP_XML = path.join(__dirname, '..', 'site-helpers', 'sitemap.xml');
const SITEMAP_HTML = path.join(__dirname, '..', 'site-helpers', 'site-map.html');

let baseUrl = 'https://timax.al';

/**
 * Parse site.md and extract pages
 */
function parseSiteMd(content) {
  const lines = content.split('\n');
  const pages = [];
  let skipUntilSeparator = true;

  for (const line of lines) {
    // Extract base URL if specified
    if (line.startsWith('Base URL:')) {
      baseUrl = line.substring(9).trim();
      continue;
    }

    // Skip everything until we hit the separator
    if (skipUntilSeparator) {
      if (line.trim() === '---') {
        skipUntilSeparator = false;
      }
      continue;
    }

    // Skip empty lines, comments, and section headers
    if (!line.trim() || line.startsWith('#')) {
      continue;
    }

    // Parse page entry: - [Title](url) | priority | changefreq
    const match = line.match(/^-\s+\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([\d.]+)\s*\|\s*(\w+)/);
    if (match) {
      pages.push({
        title: match[1].trim(),
        path: match[2].trim(),
        priority: match[3].trim(),
        changefreq: match[4].trim()
      });
    }
  }

  return pages;
}

/**
 * Generate sitemap.xml content
 */
function generateSitemapXml(pages) {
  const lastmod = new Date().toISOString().split('T')[0];
  
  let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;

  for (const page of pages) {
    const url = page.path.startsWith('http') 
      ? page.path 
      : `${baseUrl}/${page.path.replace(/^\.\//, '')}`;

    xml += `  <url>
    <loc>${url}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>
`;
  }

  xml += `</urlset>
`;

  return xml;
}

/**
 * Generate site-map.html content
 */
function generateSitemapHtml(pages) {
  // Group pages by section (extracted from site.md headers)
  const siteContent = fs.readFileSync(SITE_MD, 'utf-8');
  const lines = siteContent.split('\n');
  
  let currentSection = 'Other Pages';
  const sections = {};
  let inPagesSection = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (line.trim() === '---') {
      inPagesSection = true;
      continue;
    }

    if (!inPagesSection) continue;

    // Section header (###)
    if (line.startsWith('### ')) {
      currentSection = line.substring(4).trim();
      if (!sections[currentSection]) {
        sections[currentSection] = [];
      }
      continue;
    }

    // Page entry
    const match = line.match(/^-\s+\[([^\]]+)\]\(([^)]+)\)\s*\|/);
    if (match) {
      const page = pages.find(p => p.path === match[2].trim());
      if (page) {
        if (!sections[currentSection]) {
          sections[currentSection] = [];
        }
        sections[currentSection].push(page);
      }
    }
  }

  let html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site Map - tiMaxal Hub</title>
    <link rel="stylesheet" href="site-nav.css?v=2">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: #ccffff;
            color: #3404f4;
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.6;
            padding: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        body.dark-theme {
            background-color: #003366;
            color: #99ddff;
        }

        body.black-theme {
            background-color: #000000;
            color: #ffffff;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 30px;
        }

        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 40px;
            border-bottom: 3px solid currentColor;
            padding-bottom: 20px;
        }

        h2 {
            font-size: 1.8em;
            margin: 30px 0 15px 0;
            border-bottom: 2px solid currentColor;
            padding-bottom: 10px;
        }

        .page-list {
            list-style: none;
            margin: 20px 0 40px 20px;
        }

        .page-list li {
            margin: 12px 0;
            padding-left: 25px;
            position: relative;
        }

        .page-list li:before {
            content: "→";
            position: absolute;
            left: 0;
            font-weight: bold;
        }

        .page-list a {
            font-size: 1.1em;
            text-decoration: none;
            color: #0000ee;
            font-weight: 500;
        }

        body.dark-theme .page-list a {
            color: #66bbff;
        }

        body.black-theme .page-list a {
            color: #66bbff;
        }

        .page-list a:hover {
            text-decoration: underline;
            color: #3404f4;
        }

        body.dark-theme .page-list a:hover {
            color: #99ddff;
        }

        body.black-theme .page-list a:hover {
            color: #ffffff;
        }

        .page-description {
            font-size: 0.9em;
            opacity: 0.8;
            margin-left: 25px;
            font-style: italic;
        }

        .theme-switcher {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background-color: rgba(52, 4, 244, 0.8);
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 0.9em;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            z-index: 1000;
        }

        .theme-switcher:hover {
            transform: scale(1.05);
        }

        body.dark-theme .theme-switcher {
            background-color: rgba(153, 221, 255, 0.8);
            color: #003366;
        }

        body.black-theme .theme-switcher {
            background-color: rgba(255, 255, 255, 0.8);
            color: #000000;
        }

        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid currentColor;
        }
    </style>
    <script src="theme-switcher.js?v=2"></script>
    <script src="footer-loader.js?v=2"></script>
    <script src="site-nav.js?v=2"></script>
</head>
<body>
    <button id="themeBtn" class="theme-switcher" onclick="cycleTheme()">☀️ Light</button>
    
    <div class="container">
        <h1>📍 Site Map</h1>
        
`;

  // Generate sections
  for (const [sectionName, sectionPages] of Object.entries(sections)) {
    if (sectionPages.length === 0) continue;
    
    html += `        <h2>${sectionName}</h2>
        <ul class="page-list">
`;
    
    for (const page of sectionPages) {
      // Since site-map.html is in site-helpers/, prepend ../ to relative paths
      let adjustedPath = page.path;
      if (adjustedPath.startsWith('./')) {
        adjustedPath = '../' + adjustedPath.substring(2);
      }
      
      html += `            <li>
                <a href="${adjustedPath}">${page.title}</a>
            </li>
`;
    }
    
    html += `        </ul>
`;
  }

  html += `
        <div id="footer-container"></div>
    </div>
</body>
</html>
`;

  return html;
}

/**
 * Main function
 */
function main() {
  console.log('🗺️  Building sitemap from site.md...\n');

  // Read site.md
  if (!fs.existsSync(SITE_MD)) {
    console.error('❌ Error: site.md not found!');
    process.exit(1);
  }

  const siteContent = fs.readFileSync(SITE_MD, 'utf-8');
  
  // Parse pages
  const pages = parseSiteMd(siteContent);
  console.log(`📄 Found ${pages.length} pages to include in sitemap`);
  console.log(`🌐 Base URL: ${baseUrl}\n`);

  // Generate sitemap.xml
  const sitemapXml = generateSitemapXml(pages);
  fs.writeFileSync(SITEMAP_XML, sitemapXml, 'utf-8');
  console.log(`✅ Successfully generated sitemap.xml`);
  console.log(`📁 Output: ${SITEMAP_XML}`);

  // Generate site-map.html
  const sitemapHtml = generateSitemapHtml(pages);
  fs.writeFileSync(SITEMAP_HTML, sitemapHtml, 'utf-8');
  console.log(`✅ Successfully generated site-map.html`);
  console.log(`📁 Output: ${SITEMAP_HTML}\n`);
}

// Run
if (require.main === module) {
  main();
}

module.exports = { parseSiteMd, generateSitemapXml, generateSitemapHtml };
