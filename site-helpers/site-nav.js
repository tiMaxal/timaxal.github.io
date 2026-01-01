// Site-wide navigation
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
    currentPath = currentPath.replace(/^\/[A-Za-z]:/, '');
    const lastSlash = currentPath.lastIndexOf('/');
    const dirPath = lastSlash > 0 ? currentPath.substring(0, lastSlash) : '';
    const depth = dirPath.split('/').filter(part => part).length;
    const prefix = depth > 0 ? '../'.repeat(depth) : './';
    return buildNav(prefix);
  }
}

function buildNav(prefix) {
  const navHTML = `
    <div class="site-nav">
      <a href="${prefix}index.html" class="home-btn">🏠 Home</a>
      <div class="nav-menu" id="siteNavMenu">
        <a href="${prefix}index.html" style="font-weight: bold; border-bottom: 1px solid currentColor; margin-bottom: 10px; padding-bottom: 10px;">🏠 Home</a>
        
        <div class="nav-category">
          <h4>Main Sites</h4>
          <div class="nav-submenu">
            <a href="${prefix}aboutlife/aboutlife.html">AboutLife</a>
            <a href="https://thortz.click/" target="_blank">Thortz.Click</a>
            <a href="https://hns.au/" target="_blank">HNSau</a>
            <a href="https://registr.au/" target="_blank">registrAU</a>
            <a href="${prefix}software/software.html">Software</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>Content Pages</h4>
          <div class="nav-submenu">
            <a href="${prefix}varhns/aud/aud.html">AUD Converter</a>
            <a href="${prefix}varhns/uvau.html">UVAU</a>
            <a href="${prefix}varhns/FishingHowTo/FishingHowTo.html">FishingHowTo</a>
            <a href="${prefix}varhns/FishingHowTo/fishingame_webapp.html" style="margin-left: 15px;">→ fishinGame</a>
            <a href="${prefix}varhns/fotografi/fotografi.html">fotografi</a>
            <a href="${prefix}varhns/fotografi/cc0img.html" style="margin-left: 15px;">→ CC0 Images</a>
            <a href="${prefix}varhns/fotografi/cc-by_img.html" style="margin-left: 15px;">→ CC-BY Images</a>
            <a href="${prefix}varhns/TheBlackDog.html">TheBlackDog</a>
            <div class="nav-subcategory">
              <h5>HNS Handshake</h5>
              <a href="${prefix}sellhns/hnsell.html">Buy HNS TLDs</a>
              <a href="https://hmart/" target="_blank">HNS Merch</a>
            </div>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>Utilities</h4>
          <div class="nav-submenu">
            <a href="${prefix}site-helpers/site-map.html">Site Map</a>
          </div>
        </div>
        
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('afterbegin', navHTML);
}

// Initialize navigation on page load
document.addEventListener('DOMContentLoaded', createSiteNav);
