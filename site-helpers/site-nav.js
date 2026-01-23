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
    } else if (currentPath.includes('/HTML/varhns/aud/') || currentPath.includes('/HTML/varhns/FishingHowTo/') || currentPath.includes('/HTML/varhns/fotografi/')) {
      // We're in /HTML/varhns/[subfolder]/ (3 levels deep)
      const prefix = '../../../';
      return buildNav(prefix);
    } else if (currentPath.includes('/HTML/software/') || currentPath.includes('/HTML/aboutlife/') || currentPath.includes('/HTML/sellhns/') || currentPath.includes('/HTML/varhns/')) {
      // We're in /HTML/[folder]/ (2 levels deep)
      const prefix = '../../';
      return buildNav(prefix);
    } else if (currentPath.includes('/HTML/')) {
      // We're in /HTML/ folder (1 level deep)
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
            <a href="https://hns.au/" target="_blank">HNSau</a>
            <a href="https://registr.au/" target="_blank">registrAU</a>
            <a href="${prefix}HTML/software/software.html">Software</a>
            <a href="${prefix}HTML/varhns/aud/aud.html">AUD Converter</a>
            <a href="${prefix}HTML/varhns/uvau.html">UVAU</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>HNS Hosted Pages</h4>
          <div class="nav-submenu">
            <a href="${prefix}HTML/aboutlife/aboutlife.html">AboutLife</a>
            <a href="${prefix}HTML/sellhns/hnsell.html">Buy HNS TLDs</a>
            <a href="${prefix}HTML/sellhns/hns-merch/merchns.html">HNS Merch</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>Other Content</h4>
          <div class="nav-submenu">
            <a href="${prefix}HTML/varhns/FishingHowTo/FishingHowTo.html">FishingHowTo</a>
            <a href="${prefix}HTML/varhns/FishingHowTo/fishingame_webapp.html" style="margin-left: 15px;">→ fishinGame</a>
            <a href="${prefix}HTML/varhns/fotografi/fotografi.html">fotografi</a>
            <a href="${prefix}HTML/varhns/fotografi/cc0img.html" style="margin-left: 15px;">→ CC0 Images</a>
            <a href="${prefix}HTML/varhns/fotografi/cc-by_img.html" style="margin-left: 15px;">→ CC-BY Images</a>
            <a href="${prefix}HTML/varhns/TheBlackDog.html">TheBlackDog</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>HNS Resources</h4>
          <div class="nav-submenu">
            <a href="${prefix}HTML/sellhns/hns-tld/hns-pf.html">tiMaxal HNS TLDs</a>
            <a href="${prefix}HTML/sellhns/hns-tld/hmartld.html">Community TLD sales pages</a>
            <a href="${prefix}HTML/varhns/hnsartm/hnsartm.html">HNS art</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>Support</h4>
          <div class="nav-submenu">
            <a href="${prefix}HTML/donate.html">Donate</a>
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
