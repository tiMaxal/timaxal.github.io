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
const MENU_MD = path.join(__dirname, '..', 'site-helpers', 'md', 'menu.md');
const SITE_NAV_JS = path.join(__dirname, '..', 'HTML', 'helpers', 'site-nav.js');
const FOOTER_LOADER_JS = path.join(__dirname, '..', 'HTML', 'helpers', 'footer-loader.js');

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
    // Automatically detect depth by counting path segments
    const pathLower = currentPath.toLowerCase();
    let depth = 0;
    
    // Find the start of our site structure (after workspace root)
    // Look for /HTML/ or /site-helpers/ markers
    const htmlIndex = pathLower.lastIndexOf('/html/');
    const helpersIndex = pathLower.lastIndexOf('/site-helpers/');
    
    if (helpersIndex !== -1) {
      // Count segments after /site-helpers/
      const afterHelpers = currentPath.substring(helpersIndex + '/site-helpers/'.length);
      const segments = afterHelpers.split('/').filter(s => s && s !== 'index.html' && !s.endsWith('.html'));
      depth = segments.length + 1; // +1 for site-helpers itself
    } else if (htmlIndex !== -1) {
      // Count segments after /HTML/
      const afterHtml = currentPath.substring(htmlIndex + '/html/'.length);
      const segments = afterHtml.split('/').filter(s => s && s !== 'index.html' && !s.endsWith('.html'));
      depth = segments.length + 1; // +1 for HTML itself
    } else {
      // Root level
      depth = 0;
    }
    
    const prefix = depth > 0 ? '../'.repeat(depth) : './';
    return buildNav(prefix);
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
  const folders = { depth1: new Set(), depth2: new Set(), depth3: new Set() };
  
  for (const category of categories) {
    // Process main category items
    for (const item of category.items) {
      if (!item.isExternal) {
        // Normalize the URL by removing leading ./ or /
        const cleanUrl = item.url.replace(/^\.?\//, '');
        
        // Split into parts
        const parts = cleanUrl.split('/').filter(p => p && !p.endsWith('.html'));
        
        if (parts.length === 3) {
          // Format: folder/subfolder/subsubfolder/file.html (depth 3)
          folders.depth3.add(`/${parts[0]}/${parts[1]}/${parts[2]}/`);
        } else if (parts.length === 2) {
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
          
          if (parts.length === 3) {
            folders.depth3.add(`/${parts[0]}/${parts[1]}/${parts[2]}/`);
          } else if (parts.length === 2) {
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
    depth2: Array.from(folders.depth2).sort(),
    depth3: Array.from(folders.depth3).sort()
  };
}

/**
 * Generate footer-loader.js content based on folder structure
 */
function generateFooterLoaderJs(folders) {  // Read footer.html content
  const footerHtmlPath = path.join(__dirname, '..', 'HTML', 'helpers', 'footer.html');
  let footerContent = '';
  try {
    footerContent = fs.readFileSync(footerHtmlPath, 'utf-8').trim();
    // Replace imgs/ with ${imgPrefix} for dynamic path resolution
    footerContent = footerContent.replace(/src="imgs\//g, 'src="${imgPrefix}');
    // Replace static paths with dynamic prefix variables
    footerContent = footerContent.replace(/href="HTML\//g, 'href="${prefix}HTML/');
    footerContent = footerContent.replace(/href="site-helpers\//g, 'href="${prefix}site-helpers/');
  } catch (error) {
    console.warn(`⚠️  Warning: Could not read footer.html: ${error.message}`);
    footerContent = '<div class="footer"><p>Footer content not found</p></div>';
  }
  const depth3Checks = folders.depth3.map(f => `pathLower.includes('${f.toLowerCase()}')`).join(' ||\n        ');
  const depth2Checks = folders.depth2.map(f => `pathLower.includes('${f.toLowerCase()}')`).join(' || \n        ');
  const depth1Checks = folders.depth1.map(f => `pathLower.includes('${f.toLowerCase()}')`).join(' || \n             ');
  
  return `// Footer loader - dynamically loads footer.html into pages
function loadFooter() {
  const footerContainer = document.getElementById('footer-container');
  if (!footerContainer) return;
  
  // Determine the correct path to footer.html based on current page location
  const currentPath = window.location.pathname;
  let footerPath = 'site-helpers/footer.html';
  let imgPrefix = 'HTML/imgs/';
  
  // Automatically calculate depth
  let depth = 0;
  
  if (window.location.protocol === 'file:') {
    // Automatically detect depth by counting path segments
    const pathLower = currentPath.toLowerCase();
    
    // Find the start of our site structure
    const htmlIndex = pathLower.lastIndexOf('/html/');
    const helpersIndex = pathLower.lastIndexOf('/site-helpers/');
    
    if (helpersIndex !== -1) {
      // Count segments after /site-helpers/
      const afterHelpers = currentPath.substring(helpersIndex + '/site-helpers/'.length);
      const segments = afterHelpers.split('/').filter(s => s && !s.endsWith('.html'));
      depth = segments.length + 1;
    } else if (htmlIndex !== -1) {
      // Count segments after /HTML/
      const afterHtml = currentPath.substring(htmlIndex + '/html/'.length);
      const segments = afterHtml.split('/').filter(s => s && !s.endsWith('.html'));
      depth = segments.length + 1;
    }
  } else {
    // For HTTP/HTTPS, count directory segments from domain root
    const pathSegments = currentPath.split('/').filter(part => part && !part.includes('.html'));
    depth = pathSegments.length;
  }
  
  if (depth > 0) {
    footerPath = '../'.repeat(depth) + 'HTML/helpers/footer.html';
    imgPrefix = '../'.repeat(depth) + 'HTML/imgs/';
  }
  
  const prefix = depth > 0 ? '../'.repeat(depth) : './';
  
  // For file:// protocol, we can't use fetch, so insert the footer HTML directly
  if (window.location.protocol === 'file:') {
    const footerHTML = \`${footerContent}\`;
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
  console.log(`   - Depth 3: ${folders.depth3.join(', ') || 'none'}`);
  
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
