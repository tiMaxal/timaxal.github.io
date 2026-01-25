#!/usr/bin/env node
/**
 * Static Navigation Generator
 * Creates a simple static HTML navigation bar for no-JS fallback
 * 
 * Usage: node static-nav-builder.js
 */

const fs = require('fs');
const path = require('path');

// File paths
const OUTPUT_FILE = path.join(__dirname, '..', 'site-helpers', 'static-nav.html');

/**
 * Generate static navigation HTML snippet
 */
function generateStaticNav() {
  const html = `<!-- Static Navigation (No JavaScript Required) -->
<style>
  .static-nav {
    background-color: rgba(52, 4, 244, 0.1);
    border-bottom: 2px solid currentColor;
    padding: 10px 0;
    margin-bottom: 30px;
    text-align: center;
  }
  
  body.dark-theme .static-nav {
    background-color: rgba(153, 221, 255, 0.1);
  }
  
  body.black-theme .static-nav {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .static-nav a {
    display: inline-block;
    padding: 8px 15px;
    margin: 5px;
    text-decoration: none;
    font-weight: bold;
    border: 1px solid currentColor;
    border-radius: 5px;
    transition: all 0.2s ease;
  }
  
  .static-nav a:hover {
    background-color: currentColor;
    color: white;
  }
  
  body.dark-theme .static-nav a:hover {
    background-color: #99ddff;
    color: #003366;
  }
  
  body.black-theme .static-nav a:hover {
    background-color: #ffffff;
    color: #000000;
  }
  
  .static-nav .divider {
    display: inline-block;
    margin: 0 10px;
    opacity: 0.3;
  }
  
  /* Hide on larger screens if JS navigation is available */
  @media (min-width: 768px) {
    body.js-enabled .static-nav {
      display: none;
    }
  }
</style>

<nav class="static-nav">
  <a href="REPLACE_PREFIX_index.html">🏠 Home</a>
  <span class="divider">|</span>
  <a href="REPLACE_PREFIX_HTML/aboutlife/aboutlife.html">AboutLife</a>
  <span class="divider">|</span>
  <a href="REPLACE_PREFIX_HTML/software/software.html">Software</a>
  <span class="divider">|</span>
  <a href="REPLACE_PREFIX_HTML/sellhns/hnsell.html">HNS TLDs</a>
  <span class="divider">|</span>
  <a href="REPLACE_PREFIX_HTML/donate.html">Donate</a>
  <span class="divider">|</span>
  <a href="REPLACE_PREFIX_site-helpers/site-map.html">Site Map</a>
</nav>

<!-- Mark body as JS-enabled when JS loads -->
<script>document.body.classList.add('js-enabled');</script>
`;

  return html;
}

/**
 * Main function
 */
function main() {
  console.log('📍 Building static navigation fallback...\n');

  const html = generateStaticNav();
  
  fs.writeFileSync(OUTPUT_FILE, html, 'utf-8');
  console.log('✅ Successfully generated static-nav.html');
  console.log(`📁 Output: ${OUTPUT_FILE}\n`);
  
  console.log('💡 Usage instructions:');
  console.log('   1. Include in HTML: <!-- Static nav will be here -->');
  console.log('   2. Use footer-loader.js to insert it automatically');
  console.log('   3. Works without JavaScript!');
  console.log('   4. Auto-hides if JS navigation is available\n');
}

// Run
if (require.main === module) {
  main();
}

module.exports = { generateStaticNav };
