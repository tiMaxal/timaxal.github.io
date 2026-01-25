/**
 * Handshake New Tab Banner
 * Detects Handshake-capable browsers and displays a banner to open HNS version in a new tab.
 * Respects the site's light/dark/black theme system.
 * 
 * Usage: <script src="../../site-helpers/i2h/handshake-newtab.js" domain="aboutlife" protocol="http"></script>
 */
(function() {
  const targetDomain = document.currentScript.getAttribute('domain');
  const targetProtocol = document.currentScript.getAttribute('protocol') || 'https';
  
  // Check if browser can resolve Handshake (simple detection - not on HNS domain already)
  if (location.hostname !== targetDomain) {
    // Construct HNS URL
    const hnsUrl = `${targetProtocol}://${targetDomain}${location.pathname}`;
    
    // Create banner element
    const banner = document.createElement('div');
    banner.id = 'hns-banner';
    banner.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: rgba(52, 4, 244, 0.95);
      color: white;
      padding: 12px 20px;
      text-align: center;
      z-index: 10000;
      font-family: Arial, Helvetica, sans-serif;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
      flex-wrap: wrap;
      transition: background-color 0.3s ease;
    `;
    
    // Create banner content
    banner.innerHTML = `
      <span style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 1.2em;">🌐</span>
        <span>Handshake version available!</span>
      </span>
      <a href="${hnsUrl}" target="_blank" rel="noopener noreferrer" 
         style="
           color: #ccffff;
           font-weight: bold;
           text-decoration: underline;
           padding: 5px 15px;
           background: rgba(0, 0, 0, 0.2);
           border-radius: 4px;
           transition: background 0.2s ease;
         "
         onmouseover="this.style.background='rgba(0, 0, 0, 0.4)'"
         onmouseout="this.style.background='rgba(0, 0, 0, 0.2)'">
        Open HNS version ↗
      </a>
      <button id="hns-banner-close" 
              style="
                background: transparent;
                border: 1px solid white;
                color: white;
                cursor: pointer;
                border-radius: 3px;
                padding: 4px 12px;
                font-size: 14px;
                transition: background 0.2s ease;
                margin-left: auto;
              "
              onmouseover="this.style.background='rgba(255, 255, 255, 0.2)'"
              onmouseout="this.style.background='transparent'"
              onclick="this.parentElement.remove()">
        ✕ Dismiss
      </button>
    `;
    
    // Apply theme-aware styling
    function updateBannerTheme() {
      const currentTheme = localStorage.getItem('siteTheme') || 'light';
      
      if (currentTheme === 'dark') {
        banner.style.background = 'rgba(0, 51, 102, 0.95)';
        banner.style.borderBottom = '2px solid #66bbff';
      } else if (currentTheme === 'black') {
        banner.style.background = 'rgba(20, 20, 20, 0.98)';
        banner.style.borderBottom = '2px solid #66bbff';
      } else {
        banner.style.background = 'rgba(52, 4, 244, 0.95)';
        banner.style.borderBottom = 'none';
      }
    }
    
    // Wait for DOM to be ready before inserting banner
    function insertBanner() {
      if (document.body) {
        document.body.insertAdjacentElement('afterbegin', banner);
        updateBannerTheme();
        
        // Listen for theme changes
        const themeObserver = new MutationObserver(updateBannerTheme);
        themeObserver.observe(document.body, {
          attributes: true,
          attributeFilter: ['class']
        });
        
        // Also listen for localStorage changes (from other tabs/windows)
        window.addEventListener('storage', function(e) {
          if (e.key === 'siteTheme') {
            updateBannerTheme();
          }
        });
      }
    }
    
    // Insert banner when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', insertBanner);
    } else {
      insertBanner();
    }
  } else {
    console.log('Already on HNS domain - banner not shown');
  }
})();
