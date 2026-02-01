#!/usr/bin/env node
/**
 * Favicon Injector
 * Ensures TM.favicon.20260201.png is linked in all HTML pages.
 *
 * Usage: node favicon-builder.js
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const FAVICON_ABS = path.join(ROOT_DIR, 'HTML', 'imgs', 'TM.favicon.20260201.png');

const SKIP_DIRS = new Set(['node_modules', '.git', '__pycache__']);

function getEol(content) {
  return content.includes('\r\n') ? '\r\n' : '\n';
}

function hasHead(content) {
  return /<head[\s>]/i.test(content) && /<\/head>/i.test(content);
}

function buildFaviconTag(filePath) {
  const relPath = path
    .relative(path.dirname(filePath), FAVICON_ABS)
    .replace(/\\/g, '/');
  return `<link rel="icon" type="image/png" href="${relPath}">`;
}

function injectFavicon(content, filePath) {
  if (!hasHead(content)) return content;

  const faviconTag = buildFaviconTag(filePath);
  const eol = getEol(content);

  const iconRegex = /<link[^>]*rel=["'](?:shortcut\s+icon|icon)["'][^>]*>/i;
  if (iconRegex.test(content)) {
    return content.replace(iconRegex, faviconTag);
  }

  const headCloseRegex = new RegExp(`\\n([\\t ]*)<\\/head>`, 'i');
  const match = content.match(headCloseRegex);
  if (match) {
    const indent = match[1];
    return content.replace(
      headCloseRegex,
      `${eol}${indent}${faviconTag}${eol}${indent}</head>`
    );
  }

  return content.replace(/<\/head>/i, `${faviconTag}${eol}</head>`);
}

function collectHtmlFiles(targetPath, results) {
  if (!fs.existsSync(targetPath)) return;

  const stats = fs.statSync(targetPath);
  if (stats.isFile()) {
    if (targetPath.toLowerCase().endsWith('.html')) {
      results.add(targetPath);
    }
    return;
  }

  const entries = fs.readdirSync(targetPath, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && SKIP_DIRS.has(entry.name)) continue;

    const fullPath = path.join(targetPath, entry.name);
    if (entry.isDirectory()) {
      collectHtmlFiles(fullPath, results);
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.html')) {
      results.add(fullPath);
    }
  }
}

function main() {
  if (!fs.existsSync(FAVICON_ABS)) {
    console.error(`❌ Favicon not found: ${FAVICON_ABS}`);
    process.exit(1);
  }

  const htmlFiles = new Set();
  collectHtmlFiles(path.join(ROOT_DIR, 'index.html'), htmlFiles);
  collectHtmlFiles(path.join(ROOT_DIR, 'HTML'), htmlFiles);
  collectHtmlFiles(path.join(ROOT_DIR, 'site-helpers'), htmlFiles);

  let updated = 0;
  for (const filePath of htmlFiles) {
    const original = fs.readFileSync(filePath, 'utf-8');
    const next = injectFavicon(original, filePath);
    if (next !== original) {
      fs.writeFileSync(filePath, next, 'utf-8');
      updated += 1;
    }
  }

  console.log(`✅ Favicon updated in ${updated} file(s).`);
}

if (require.main === module) {
  main();
}
