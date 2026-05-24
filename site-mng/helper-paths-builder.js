#!/usr/bin/env node
/**
 * Helper Paths Builder
 * Ensures site-nav.css, theme-switcher.js, footer-loader.js, and site-nav.js
 * are referenced with the correct relative path in every HTML page that already
 * includes them, and ensures the favicon link is present/correct.
 *
 * Helper tags are only repaired when already present (no helper-tag injection),
 * while favicon is injected/replaced in any page with a <head> section.
 *
 * Usage: node helper-paths-builder.js
 */

const fs   = require('fs');
const path = require('path');

const ROOT_DIR   = path.join(__dirname, '..');
const HELPERS_DIR = path.join(ROOT_DIR, 'HTML', 'helpers');
const FAVICON_ABS = path.join(ROOT_DIR, 'HTML', 'imgs', 'TM.favicon.20260201.png');

const SKIP_DIRS  = new Set(['node_modules', '.git', '__pycache__', 'old-helpers']);
// template.html is a build source read by md-to-html.js; its paths must stay
// as the canonical "HTML/helpers/" literal so md-to-html.js can pattern-match them.
const SKIP_FILES = new Set([
  path.join(ROOT_DIR, 'site-helpers', 'template.html'),
]);

// ---------------------------------------------------------------------------
// Helper asset definitions
// Each entry describes one shared resource, how to detect it in HTML source,
// and how to build the canonical corrected tag.
// ---------------------------------------------------------------------------
const HELPERS = [
  {
    filename : 'site-nav.css',
    // Matches:  <link ... href="<anything>site-nav.css<anything>" ...>
    pattern  : /<link\b[^>]*\bhref="[^"]*site-nav\.css(?:\?[^"]*)?"[^>]*\/?>/i,
    buildTag : (rel) => `<link rel="stylesheet" href="${rel}?v=2">`,
  },
  {
    filename : 'theme-switcher.js',
    // Matches:  <script ... src="<anything>theme-switcher.js<anything>"></script>
    pattern  : /<script\b[^>]*\bsrc="[^"]*theme-switcher\.js(?:\?[^"]*)?"[^>]*>\s*<\/script>/i,
    buildTag : (rel) => `<script src="${rel}?v=2"></script>`,
  },
  {
    filename : 'footer-loader.js',
    pattern  : /<script\b[^>]*\bsrc="[^"]*footer-loader\.js(?:\?[^"]*)?"[^>]*>\s*<\/script>/i,
    buildTag : (rel) => `<script src="${rel}?v=2"></script>`,
  },
  {
    filename : 'site-nav.js',
    // Use word boundary on "site-nav.js" so it doesn't accidentally match inside
    // site-nav.css lines (both contain "site-nav" but differ after the dot).
    pattern  : /<script\b[^>]*\bsrc="[^"]*site-nav\.js(?:\?[^"]*)?"[^>]*>\s*<\/script>/i,
    buildTag : (rel) => `<script src="${rel}?v=2"></script>`,
  },
];

// ---------------------------------------------------------------------------
// Core logic
// ---------------------------------------------------------------------------

/**
 * Return the correct relative path from filePath's directory to the helpers dir,
 * using forward slashes.
 */
function relativeHelpersDir(filePath) {
  return path.relative(path.dirname(filePath), HELPERS_DIR).replace(/\\/g, '/');
}

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

/**
 * Fix helper-script paths in one HTML file.
 * Returns the (possibly updated) content string.
 */
function fixHelperPaths(content, filePath) {
  if (SKIP_FILES.has(filePath)) return content;

  const helpersRel = relativeHelpersDir(filePath);

  for (const helper of HELPERS) {
    if (!helper.pattern.test(content)) continue; // tag not present — skip

    const correctTag = helper.buildTag(`${helpersRel}/${helper.filename}`);
    content = content.replace(helper.pattern, correctTag);
  }

  return content;
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

// ---------------------------------------------------------------------------
// File collection
// ---------------------------------------------------------------------------

function collectHtmlFiles(targetPath, results) {
  if (!fs.existsSync(targetPath)) return;

  const stats = fs.statSync(targetPath);
  if (stats.isFile()) {
    if (targetPath.toLowerCase().endsWith('.html') && !SKIP_FILES.has(targetPath)) {
      results.add(targetPath);
    }
    return;
  }

  for (const entry of fs.readdirSync(targetPath, { withFileTypes: true })) {
    if (entry.isDirectory() && SKIP_DIRS.has(entry.name)) continue;
    const fullPath = path.join(targetPath, entry.name);
    if (entry.isDirectory()) {
      collectHtmlFiles(fullPath, results);
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.html') && !SKIP_FILES.has(fullPath)) {
      results.add(fullPath);
    }
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  if (!fs.existsSync(FAVICON_ABS)) {
    console.error(`❌ Favicon not found: ${FAVICON_ABS}`);
    process.exit(1);
  }

  const htmlFiles = new Set();
  collectHtmlFiles(path.join(ROOT_DIR, 'index.html'), htmlFiles);
  collectHtmlFiles(path.join(ROOT_DIR, 'HTML'), htmlFiles);
  collectHtmlFiles(path.join(ROOT_DIR, 'site-helpers'), htmlFiles);

  let helperUpdated = 0;
  let faviconUpdated = 0;

  for (const filePath of htmlFiles) {
    const original = fs.readFileSync(filePath, 'utf-8');
    const helperFixed = fixHelperPaths(original, filePath);
    const faviconFixed = injectFavicon(helperFixed, filePath);

    if (helperFixed !== original) {
      helperUpdated += 1;
    }
    if (faviconFixed !== helperFixed) {
      faviconUpdated += 1;
    }

    if (faviconFixed !== original) {
      fs.writeFileSync(filePath, faviconFixed, 'utf-8');
      console.log(`  ↳ fixed: ${path.relative(ROOT_DIR, filePath).replace(/\\/g, '/')}`);
    }
  }

  console.log(
    `✅ Helper paths updated in ${helperUpdated} file(s); favicon updated in ${faviconUpdated} file(s).`
  );
}

module.exports = { main };

if (require.main === module) {
  main();
}
