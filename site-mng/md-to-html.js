#!/usr/bin/env node
/**
 * Markdown to HTML Converter Script
 * Converts markdown files from site-helpers/md/ to HTML with site navigation and footer
 * 
 * Usage: node md-to-html.js [--all | specific-file.md]
 */

const fs = require('fs');
const path = require('path');
const { marked } = require('../site-helpers/node_modules/marked');

// File paths
const MD_DIR = path.join(__dirname, '..', 'site-helpers', 'md', 'md-new');
const HTML_OUTPUT_DIR = path.join(__dirname, '..', 'HTML');
const TEMPLATE_FILE = path.join(__dirname, '..', 'site-helpers', 'template.html');

/**
 * Read template and extract styles section
 */
function readTemplate() {
  if (!fs.existsSync(TEMPLATE_FILE)) {
    console.error('❌ Error: template.html not found!');
    process.exit(1);
  }
  return fs.readFileSync(TEMPLATE_FILE, 'utf-8');
}

/**
 * Extract frontmatter from markdown content
 * Frontmatter format:
 * ---
 * title: Page Title
 * path: subfolder/page.html (relative to HTML/)
 * ---
 */
function parseFrontmatter(content) {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n/;
  const match = content.match(frontmatterRegex);
  
  if (!match) {
    return { frontmatter: {}, content };
  }
  
  const frontmatterLines = match[1].split('\n');
  const frontmatter = {};
  
  for (const line of frontmatterLines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim();
      frontmatter[key] = value;
    }
  }
  
  const contentWithoutFrontmatter = content.replace(frontmatterRegex, '');
  return { frontmatter, content: contentWithoutFrontmatter };
}

/**
 * Calculate relative path to site-helpers based on output location
 */
function getRelativePath(outputPath) {
  const outputDir = path.dirname(outputPath);
  const siteHelpersPath = path.join(__dirname, '..', 'site-helpers');
  const relativePath = path.relative(outputDir, siteHelpersPath);
  return relativePath.replace(/\\/g, '/');
}

/**
 * Convert markdown to HTML using template
 */
function convertMdToHtml(mdPath, outputPath = null) {
  console.log(`📄 Processing: ${path.basename(mdPath)}`);
  
  // Read markdown file
  const mdContent = fs.readFileSync(mdPath, 'utf-8');
  
  // Parse frontmatter
  const { frontmatter, content } = parseFrontmatter(mdContent);
  
  // Determine output path
  if (!outputPath) {
    if (frontmatter.path) {
      outputPath = path.join(HTML_OUTPUT_DIR, frontmatter.path);
    } else {
      // Default: same name, in root HTML folder
      const htmlFilename = path.basename(mdPath).replace(/\.md$/, '.html');
      outputPath = path.join(HTML_OUTPUT_DIR, htmlFilename);
    }
  }
  
  // Get page title
  const title = frontmatter.title || 'Page Title';
  
  // Convert markdown to HTML
  const htmlBody = marked.parse(content);
  
  // Read template
  const template = readTemplate();
  
  // Calculate relative paths for scripts/styles
  const relativePath = getRelativePath(outputPath);
  
  // Build complete HTML
  let html = template;
  
  // Replace title
  html = html.replace('<title>Page Title - tiMaxal Hub</title>', 
                      `<title>${title} - tiMaxal Hub</title>`);
  
  // Extract the content area from template and replace with markdown content
  // Find the main content section (between <div class="container"> and footer)
  const contentStartMarker = '<!-- ✏️ EDIT: Add your main content below -->';
  const contentEndMarker = '<!-- ⚙️ DO NOT EDIT: Footer container';
  
  const contentStart = html.indexOf(contentStartMarker);
  const contentEnd = html.indexOf(contentEndMarker);
  
  if (contentStart !== -1 && contentEnd !== -1) {
    const beforeContent = html.substring(0, contentStart + contentStartMarker.length);
    const afterContent = html.substring(contentEnd);
    
    html = beforeContent + '\n\n' + htmlBody + '\n\n        ' + afterContent;
  }
  
  // Update script paths based on output location depth
  // Template has "HTML/helpers/" for root level (index.html)
  // Generated pages in HTML/ need "helpers/"
  // Generated pages in HTML/subfolder/ need "../helpers/"
  const depth = outputPath.split(path.sep).length - HTML_OUTPUT_DIR.split(path.sep).length - 1;
  let pathPrefix = 'helpers/';
  if (depth > 0) {
    pathPrefix = '../'.repeat(depth) + 'helpers/';
  }
  
  // Replace template's HTML/helpers/ pattern (for pages generated into HTML/ folder)
  html = html.replace(/href="HTML\/helpers\//g, `href="${pathPrefix}`);
  html = html.replace(/src="HTML\/helpers\//g, `src="${pathPrefix}`);
  
  // Create output directory if needed
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Write HTML file
  fs.writeFileSync(outputPath, html, 'utf-8');
  console.log(`✅ Generated: ${outputPath}`);
  
  return outputPath;
}

/**
 * Find all markdown files in MD_DIR
 */
function findMarkdownFiles(dir = MD_DIR) {
  const files = [];
  
  if (!fs.existsSync(dir)) {
    return files;
  }
  
  function recurse(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      
      if (entry.isDirectory()) {
        recurse(fullPath);
      } else if (entry.name.endsWith('.md')) {
        files.push(fullPath);
      }
    }
  }
  
  recurse(dir);
  return files;
}

/**
 * Main function
 */
function main() {
  const args = process.argv.slice(2);
  
  console.log('📝 Markdown to HTML Converter\n');
  
  // Check if MD directory exists
  if (!fs.existsSync(MD_DIR)) {
    console.log(`📁 Creating directory: ${MD_DIR}`);
    fs.mkdirSync(MD_DIR, { recursive: true });
    
    // Create example markdown file
    const exampleMd = `---
title: Example Page
path: example.html
---

# Example Page

This is an example page created from markdown.

## Features

- **Easy to write**: Just use markdown syntax
- **Automatic navigation**: Site menu is added automatically
- **Theme support**: Works with Light/Dark/Black themes
- **Responsive**: Mobile-friendly design

## Getting Started

1. Create a new .md file in site-helpers/md/
2. Add frontmatter with title and path
3. Write your content in markdown
4. Run: node md-to-html.js --all

Your HTML page will be generated with full site navigation!
`;
    
    const examplePath = path.join(MD_DIR, 'example.md');
    fs.writeFileSync(examplePath, exampleMd, 'utf-8');
    console.log(`📄 Created example file: ${examplePath}\n`);
  }
  
  // Process files
  if (args.includes('--all') || args.length === 0) {
    const mdFiles = findMarkdownFiles();
    
    if (mdFiles.length === 0) {
      console.log('ℹ️  No markdown files found in site-helpers/md/');
      console.log('   Create .md files there to get started!\n');
      return;
    }
    
    console.log(`📄 Found ${mdFiles.length} markdown file(s)\n`);
    
    for (const mdFile of mdFiles) {
      convertMdToHtml(mdFile);
    }
    
    console.log('\n✅ All files processed successfully!');
  } else {
    // Process specific file
    const inputFile = args[0];
    const mdPath = path.isAbsolute(inputFile) 
      ? inputFile 
      : path.join(MD_DIR, inputFile);
    
    if (!fs.existsSync(mdPath)) {
      console.error(`❌ Error: File not found: ${mdPath}`);
      process.exit(1);
    }
    
    convertMdToHtml(mdPath);
    console.log('\n✅ File processed successfully!');
  }
}

// Run
if (require.main === module) {
  main();
}

module.exports = { convertMdToHtml, findMarkdownFiles, parseFrontmatter };
