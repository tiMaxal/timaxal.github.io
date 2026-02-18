// Site-wide navigation
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
          <h4>Main Pages</h4>
          <div class="nav-submenu">
            <a href="https://hns.au/" target="_blank">HNSau</a>
            <a href="https://registr.au/" target="_blank">registrAU</a>
            <a href="${prefix}HTML/software/software.html">Software</a>
            <a href="${prefix}HTML/varhns/aud/aud.html">AUD Converter</a>
            <a href="${prefix}HTML/varhns/uvau.html">UVAU</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>Other Content</h4>
          <div class="nav-submenu">
            <a href="${prefix}HTML/varhns/health.html">Health</a>
            <a href="${prefix}HTML/aboutlife/aboutlife.html" style="margin-left: 15px;">→ AboutLife</a>
            <a href="${prefix}HTML/varhns/digi-det0x.html" style="margin-left: 15px;">→ digital.det0x</a>
            <a href="${prefix}HTML/varhns/TheBlackDog.html" style="margin-left: 15px;">→ TheBlackDog</a>
            <a href="${prefix}HTML/varhns/FishingHowTo/FishingHowTo.html">FishingHowTo</a>
            <a href="${prefix}HTML/varhns/FishingHowTo/fishingame_webapp.html" style="margin-left: 15px;">→ fishinGame</a>
            <a href="${prefix}HTML/varhns/fotografi/fotografi.html">fotografi</a>
            <a href="${prefix}HTML/varhns/fotografi/cc0img.html" style="margin-left: 15px;">→ CC0 Images</a>
            <a href="${prefix}HTML/varhns/fotografi/cc-by_img.html" style="margin-left: 15px;">→ CC-BY Images</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>HNS Resources</h4>
          <div class="nav-submenu">
            <a href="${prefix}HTML/sellhns/hnsell.html">Buy HNS TLDs</a>
            <a href="${prefix}HTML/sellhns/hns-tld/hmartld.html" style="margin-left: 15px;">→ Community TLD sales pages</a>
            <a href="${prefix}HTML/sellhns/hns-tld/hns-pf.html" style="margin-left: 15px;">→ tiMaxal HNS TLDs</a>
            <a href="${prefix}HTML/sellhns/hns-merch/merchns.html">HNS Merch</a>
            <a href="${prefix}HTML/varhns/hnsartm/hnsartm.html">HNS art</a>
          </div>
        </div>
        
        <div class="nav-category">
          <h4>Utilities</h4>
          <div class="nav-submenu">
            <a href="${prefix}HTML/donate.html">Donate</a>
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
