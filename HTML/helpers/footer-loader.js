// Footer loader - dynamically loads footer.html into pages
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
    const footerHTML = `
      <div class="footer">
        <p>
          <a href="https://hns.au" target="_blank">
            <img src="${imgPrefix}hnsau_blak-H-trans-bak+gg-centre_60x60.webp" alt="Handshake Australia" height="50" width="50" class="footer-logo">
          </a>
        </p>
        <p style="margin-top: 15px;">
          <a href="https://discord.gg/2SaK36G5eU" target="_blank">
            <img src="${imgPrefix}MaxPixel.Logo-Discord-6062232.CC0.png" alt="Discord" height="20" width="20">
          </a>
          <a href="https://www.facebook.com/people/HNS-AU/100086556653400/" target="_blank">
            <img src="${imgPrefix}fb-web.svg" alt="Facebook" height="20" width="20">
          </a>
          <a href="https://twitter.com/tiMaxal" target="_blank">
            <img src="${imgPrefix}Twitter.svg" alt="Twitter" height="20" width="20">
          </a>
        </p>
        <p style="margin-top: 10px; font-size: 0.9em;">
          <a href="${prefix}HTML/donate.html">💝 Support / Donate</a> • 
          <a href="${prefix}site-helpers/site-map.html">🗺️ Site Map</a>
        </p>
        <h6 style="margin-top: 20px; font-size: 0.8em; opacity: 0.8;">© 2026 tiMaxal</h6>
      </div>
    `;
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
