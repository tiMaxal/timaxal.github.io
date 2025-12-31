#!/usr/bin/env node
/**
 * Menu Builder Script
 * Converts menu.md to site-nav.js
 * 
 * Usage: node menu-builder.js
 */

const fs = require('fs');
const path = require('path');

// File paths
const MENU_MD = path.join(__dirname, 'menu.md');
const SITE_NAV_JS = path.join(__dirname, '..', 'site-helpers', 'site-nav.js');
const FOOTER_LOADER_JS = path.join(__dirname, '..', 'site-helpers', 'footer-loader.js');

/**
 * Parse menu.md and convert to navigation structure
 */
function parseMenuMd(content) {
  const lines = content.split('\n');
  const categories = [];
  let currentCategory = null;
  let currentSubCategory = null;
  let skipUntilSeparator = true;

  for (const line of lines) {
    // Skip everything until we hit the separator
    if (skipUntilSeparator) {
      if (line.trim() === '---') {
        skipUntilSeparator = false;
      }
      continue;
    }

    // Skip empty lines and comments
    if (!line.trim() || line.startsWith('#') && !line.startsWith('##') && !line.startsWith('###')) {
      continue;
    }

    // Category header (## Header)
    if (line.startsWith('## ')) {
      currentCategory = {
        name: line.substring(3).trim(),
        items: [],
        subCategories: []
      };
      categories.push(currentCategory);
      currentSubCategory = null;
      continue;
    }

    // Sub-category header (### Header)
    if (line.startsWith('### ')) {
      if (currentCategory) {
        currentSubCategory = {
          name: line.substring(4).trim(),
          items: []
        };
        currentCategory.subCategories.push(currentSubCategory);
      }
      continue;
    }

    // Menu item
    const linkMatch = line.match(/^(\s*)- \[([^\]]+)\]\(([^)]+)\)(\s*\{external\})?/);
    if (linkMatch && currentCategory) {
      const indent = linkMatch[1].length;
      const text = linkMatch[2];
      const url = linkMatch[3];
      const isExternal = !!linkMatch[4];
      
      // Get description (next line that doesn't start with - or whitespace+-)
      const currentIndex = lines.indexOf(line);
      let description = '';
      if (currentIndex + 1 < lines.length) {
        const nextLine = lines[currentIndex + 1];
        if (nextLine.trim() && !nextLine.trim().startsWith('-')) {
          description = nextLine.trim();
        }
      }

      const item = {
        text,
        url,
        isExternal,
        isSubItem: indent > 0,
        description
      };

      // Add to sub-category if we're in one, otherwise to main category
      if (currentSubCategory) {
        currentSubCategory.items.push(item);
      } else {
        currentCategory.items.push(item);
      }
    }
  }

  return categories;
}

/**
 * Generate site-nav.js content from navigation structure
 */
function generateSiteNavJs(categories) {
  let js = `// Site-wide navigation
function createSiteNav() {
  // Get the current file path and normalize it
  let currentPath = window.location.pathname;
  
  // For file:// protocol, handle Windows paths differently
  if (window.location.protocol === 'file:') {
    // Get just the filename from the full path
    const parts = currentPath.split('/');
    const fileName = parts[parts.length - 1];
    
    // Determine depth by counting parent directories
    // Check which folder we're in by looking at the path structure
    if (currentPath.includes('/site-helpers/')) {
      // We're in /site-helpers/ folder (1 level deep)
      const prefix = '../';
      return buildNav(prefix);
    } else if (currentPath.includes('/software/')) {
      // We're in /software/ folder (1 level deep)
      const prefix = '../';
      return buildNav(prefix);
    } else if (currentPath.includes('/aboutlife/')) {
      // We're in /aboutlife/ folder (1 level deep)
      const prefix = '../';
      return buildNav(prefix);
    } else if (currentPath.includes('/sellhns/')) {
      // We're in /sellhns/ folder (1 level deep)
      const prefix = '../';
      return buildNav(prefix);
    } else if (currentPath.includes('/varhns/aud/')) {
      // We're in /varhns/aud/ folder (2 levels deep)
      const prefix = '../../';
      return buildNav(prefix);
    } else if (currentPath.includes('/varhns/FishingHowTo/')) {
      // We're in /varhns/FishingHowTo/ folder (2 levels deep)
      const prefix = '../../';
      return buildNav(prefix);
    } else if (currentPath.includes('/varhns/fotografi/')) {
      // We're in /varhns/fotografi/ folder (2 levels deep)
      const prefix = '../../';
      return buildNav(prefix);
    } else if (currentPath.includes('/varhns/')) {
      // We're in /varhns/ folder (1 level deep)
      const prefix = '../';
      return buildNav(prefix);
    } else {
      // We're in root
      const prefix = './';
      return buildNav(prefix);
    }
  } else {
    // For HTTP/HTTPS, use normal path calculation
    currentPath = currentPath.replace(/^\\/[A-Za-z]:/, '');
    const lastSlash = currentPath.lastIndexOf('/');
    const dirPath = lastSlash > 0 ? currentPath.substring(0, lastSlash) : '';
    const depth = dirPath.split('/').filter(part => part).length;
    const prefix = depth > 0 ? '../'.repeat(depth) : './';
    return buildNav(prefix);
  }
}

function buildNav(prefix) {
  const navHTML = \`
    <div class="site-nav">
      <a href="\${prefix}index.html" class="home-btn">🏠 Home</a>
      <div class="nav-menu" id="siteNavMenu">
        <a href="\${prefix}index.html" style="font-weight: bold; border-bottom: 1px solid currentColor; margin-bottom: 10px; padding-bottom: 10px;">🏠 Home</a>
        \n`;

  for (const category of categories) {
    js += `        <div class="nav-category">
          <h4>${category.name}</h4>
          <div class="nav-submenu">\n`;

    // Add main category items
    for (const item of category.items) {
      // Remove leading ./ from paths since prefix will handle it
      const cleanPath = item.url.replace(/^\.\//, '');
      const href = item.isExternal ? item.url : `\${prefix}${cleanPath}`;
      const target = item.isExternal ? ' target="_blank"' : '';
      const style = item.isSubItem ? ' style="margin-left: 15px;"' : '';
      const arrow = item.isSubItem ? '→ ' : '';
      
      js += `            <a href="${href}"${target}${style}>${arrow}${item.text}</a>\n`;
    }

    // Add sub-categories
    for (const subCat of category.subCategories) {
      js += `            <div class="nav-subcategory">
              <h5>${subCat.name}</h5>\n`;
      
      for (const item of subCat.items) {
        const cleanPath = item.url.replace(/^\.\//, '');
        const href = item.isExternal ? item.url : `\${prefix}${cleanPath}`;
        const target = item.isExternal ? ' target="_blank"' : '';
        const style = item.isSubItem ? ' style="margin-left: 15px;"' : '';
        const arrow = item.isSubItem ? '→ ' : '';
        
        js += `              <a href="${href}"${target}${style}>${arrow}${item.text}</a>\n`;
      }
      
      js += `            </div>\n`;
    }

    js += `          </div>
        </div>
        \n`;
  }

  js += `      </div>
    </div>
  \`;
  
  document.body.insertAdjacentHTML('afterbegin', navHTML);
}

// Initialize navigation on page load
document.addEventListener('DOMContentLoaded', createSiteNav);
`;

  return js;
}

/**Extract folder structure from menu links
 */
function extractFolderStructure(categories) {
  const folders = { depth1: new Set(), depth2: new Set() };
  
  for (const category of categories) {
    // Process main category items
    for (const item of category.items) {
      if (!item.isExternal) {
        // Normalize the URL by removing leading ./ or /
        const cleanUrl = item.url.replace(/^\.?\//, '');
        
        // Split into parts
        const parts = cleanUrl.split('/').filter(p => p && !p.endsWith('.html'));
        
        if (parts.length === 2) {
          // Format: folder/subfolder/file.html (depth 2)
          folders.depth2.add(`/${parts[0]}/${parts[1]}/`);
        } else if (parts.length === 1) {
          // Format: folder/file.html (depth 1)
          folders.depth1.add(`/${parts[0]}/`);
        }
      }
    }
    
    // Process sub-category items
    for (const subCat of category.subCategories) {
      for (const item of subCat.items) {
        if (!item.isExternal) {
          const cleanUrl = item.url.replace(/^\.?\//, '');
          const parts = cleanUrl.split('/').filter(p => p && !p.endsWith('.html'));
          
          if (parts.length === 2) {
            folders.depth2.add(`/${parts[0]}/${parts[1]}/`);
          } else if (parts.length === 1) {
            folders.depth1.add(`/${parts[0]}/`);
          }
        }
      }
    }
  }
  
  return {
    depth1: Array.from(folders.depth1).sort(),
    depth2: Array.from(folders.depth2).sort()
  };
}

/**
 * Generate footer-loader.js content based on folder structure
 */
function generateFooterLoaderJs(folders) {
  const depth2Checks = folders.depth2.map(f => `pathLower.includes('${f.toLowerCase()}')`).join(' || \n        ');
  const depth1Checks = folders.depth1.map(f => `pathLower.includes('${f.toLowerCase()}')`).join(' || \n             ');
  
  return `// Footer loader - dynamically loads footer.html into pages
function loadFooter() {
  const footerContainer = document.getElementById('footer-container');
  if (!footerContainer) return;
  
  // Determine the correct path to footer.html based on current page location
  const currentPath = window.location.pathname;
  let footerPath = 'footer.html';
  let imgPrefix = 'imgs/';
  
  // Automatically calculate depth
  let depth = 0;
  
  if (window.location.protocol === 'file:') {
    // For file://, detect depth by checking which folders are in the path
    // This is auto-generated from menu.md by menu-builder.js
    const pathLower = currentPath.toLowerCase();
    
    // Check for 2-level deep folders (must check these first!)
    if (${depth2Checks || 'false'}) {
      depth = 2;
    }
    // Check for 1-level deep folders
    else if (${depth1Checks || 'false'}) {
      depth = 1;
    }
    // Otherwise we're at root (depth = 0)
  } else {
    // For HTTP/HTTPS, count directory segments from domain root
    const pathSegments = currentPath.split('/').filter(part => part && !part.includes('.html'));
    depth = pathSegments.length;
  }
  
  if (depth > 0) {
    footerPath = '../'.repeat(depth) + 'footer.html';
    imgPrefix = '../'.repeat(depth) + 'imgs/';
  }
  
  // For file:// protocol, we can't use fetch, so insert the footer HTML directly
  if (window.location.protocol === 'file:') {
    const footerHTML = \`
<div class="footer">
  <p>
    <a href="https://hns.au" target="_blank">
      <img src="\${imgPrefix}hnsau_blak-H-trans-bak+gg-centre_60x60.webp" alt="Handshake Australia" height="50" width="50">
    </a>
  </p>
  <p style="margin-top: 15px;">
    <a href="https://discord.gg/uKV5yKyBHG" target="_blank">
      <img src="\${imgPrefix}MaxPixel.Logo-Discord-6062232.CC0.png" alt="Handshake Australia Community Discord" height="20" width="20">
    </a>
    <a href="https://www.facebook.com/people/HNS-AU/100086556653400/" target="_blank">
      <img src="\${imgPrefix}fb-web.svg" alt="HNSau@fb.com" height="20" width="20">
    </a>
    <a href="https://twitter.com/tiMaxal" target="_blank">
      <img src="\${imgPrefix}Twitter.svg" alt="@tiMaxal" height="20" width="20">
    </a>
  </p>
  <h6>[a <a href="https://timax.au/" target="_blank">tiMaxal</a> enterprises offering]</h6>
</div>\`;
    footerContainer.innerHTML = footerHTML;
  } else {
    // For HTTP/HTTPS, use fetch
    fetch(footerPath)
      .then(response => response.text())
      .then(html => {
        footerContainer.innerHTML = html;
        
        // Fix image paths after loading
        const images = footerContainer.querySelectorAll('img');
        images.forEach(img => {
          const src = img.getAttribute('src');
          if (src && src.startsWith('imgs/')) {
            img.src = imgPrefix + src.substring(5);
          }
        });
      })
      .catch(error => console.error('Error loading footer:', error));
  }
}

// Load footer when DOM is ready
document.addEventListener('DOMContentLoaded', loadFooter);
`;
}

/**
 * Main function
 */
function main() {
  console.log('🔧 Building site navigation from menu.md...\n');

  // Read menu.md
  if (!fs.existsSync(MENU_MD)) {
    console.error('❌ Error: menu.md not found!');
    process.exit(1);
  }

  const menuContent = fs.readFileSync(MENU_MD, 'utf-8');
  
  // Parse and generate
  const categories = parseMenuMd(menuContent);
  console.log(`📋 Found ${categories.length} menu categories:`);
  categories.forEach(cat => {
    console.log(`   - ${cat.name} (${cat.items.length} items)`);
  });

  const siteNavJs = generateSiteNavJs(categories);
  
  // Write site-nav.js
  fs.writeFileSync(SITE_NAV_JS, siteNavJs, 'utf-8');
  console.log(`\n✅ Successfully generated site-nav.js`);
  console.log(`📁 Output: ${SITE_NAV_JS}`);
  
  // Extract folder structure and generate footer-loader.js
  const folders = extractFolderStructure(categories);
  console.log(`\n📁 Detected folder structure:`);
  console.log(`   - Depth 1: ${folders.depth1.join(', ') || 'none'}`);
  console.log(`   - Depth 2: ${folders.depth2.join(', ') || 'none'}`);
  
  const footerLoaderJs = generateFooterLoaderJs(folders);
  fs.writeFileSync(FOOTER_LOADER_JS, footerLoaderJs, 'utf-8');
  console.log(`\n✅ Successfully generated footer-loader.js`);
  console.log(`📁 Output: ${FOOTER_LOADER_JS}\n`);
}

// Run
if (require.main === module) {
  main();
}

module.exports = { parseMenuMd, generateSiteNavJs, extractFolderStructure, generateFooterLoaderJs };
