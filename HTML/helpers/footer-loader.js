// Footer loader - dynamically loads footer.html into pages
function loadFooter() {
  const footerContainer = document.getElementById('footer-container');
  if (!footerContainer) return;
  
  // Determine the correct path to footer.html based on current page location
  const currentPath = window.location.pathname;
  let footerPath = 'HTML/helpers/footer.html';
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
      // Count segments after /HTML/ (plus 1 for HTML folder itself to reach root)
      const afterHtml = currentPath.substring(htmlIndex + '/html/'.length);
      const segments = afterHtml.split('/').filter(s => s && !s.endsWith('.html'));
      depth = segments.length + 1;
    }
  } else {
    // For HTTP/HTTPS, count directory segments from domain root
    const pathSegments = currentPath.split('/').filter(part => part && !part.includes('.html'));
    depth = pathSegments.length;
    
    // Special handling for HTTP/HTTPS: check if we're inside HTML folder
    const isInHtmlFolder = pathSegments.length > 0 && pathSegments[0].toLowerCase() === 'html';
    if (isInHtmlFolder) {
      // Inside HTML folder: adjust paths to be relative to HTML folder
      const depthInHtml = pathSegments.length - 1;
      footerPath = (depthInHtml > 0 ? '../'.repeat(depthInHtml) : '') + 'helpers/footer.html';
      imgPrefix = (depthInHtml > 0 ? '../'.repeat(depthInHtml) : '') + 'imgs/';
      // For links, go back to HTML folder root, then to target
      depth = depthInHtml; // Reset depth for prefix calculation
    } else {
      // Outside HTML folder (e.g., root): use path from root
      if (depth > 0) {
        footerPath = '../'.repeat(depth) + 'HTML/helpers/footer.html';
        imgPrefix = '../'.repeat(depth) + 'HTML/imgs/';
      } else {
        // At root level - use absolute path from domain root for HTTP/HTTPS
        footerPath = '/HTML/helpers/footer.html';
        imgPrefix = '/HTML/imgs/';
      }
    }
  }
  
  // For file:// protocol, override with file-specific paths
  if (window.location.protocol === 'file:' && depth > 0) {
    footerPath = '../'.repeat(depth) + 'HTML/helpers/footer.html';
    imgPrefix = '../'.repeat(depth) + 'HTML/imgs/';
  }
  
  // Calculate prefix for internal links
  let prefix;
  if (window.location.protocol !== 'file:') {
    // For HTTP/HTTPS at root level, use absolute paths
    const pathSegments = currentPath.split('/').filter(part => part && !part.includes('.html'));
    const isRoot = pathSegments.length === 0;
    prefix = isRoot ? '/' : (depth > 0 ? '../'.repeat(depth) : './');
  } else {
    prefix = depth > 0 ? '../'.repeat(depth) : './';
  }
  
  // For file:// protocol, we can't use fetch, so insert the footer HTML directly
  if (window.location.protocol === 'file:') {
    const footerHTML = `<div class="footer">
  <p>
    <a href="https://hns.au" target="_blank">
      <img src="${imgPrefix}hnsau_blak-H-trans-bak+gg-centre_60x60.webp" alt="Handshake Australia" height="50" width="50" class="footer-logo">
    </a>
  </p>
  <p style="margin-top: 15px;">
    <a href="https://discord.gg/jc5vUk3j3y" target="_blank">
      <img src="${imgPrefix}MaxPixel.Logo-Discord-6062232.CC0.png" alt="Handshake Australia Community Discord" height="20" width="20">
    </a>
    <a href="https://www.facebook.com/people/HNS-AU/100086556653400/" target="_blank">
      <img src="${imgPrefix}fb-web.svg" alt="HNSau@fb.com" height="20" width="20">
    </a>
    <a href="https://twitter.com/tiMaxal" target="_blank">
      <img src="${imgPrefix}Twitter.svg" alt="@tiMaxal" height="20" width="20">
    </a>
  </p>
  <p style="margin-top: 10px; font-size: 0.9em;">
    <a href="${prefix}HTML/donate.html">💝 Support / Donate</a> • 
    <a href="${prefix}site-helpers/site-map.html">🗺️ Site Map</a>`;
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
        
        // Fix internal link paths after loading
        const pathSegments = window.location.pathname.split('/').filter(part => part && !part.includes('.html'));
        const isInHtmlFolder = pathSegments.length > 0 && pathSegments[0].toLowerCase() === 'html';
        const depthInHtml = isInHtmlFolder ? pathSegments.length - 1 : 0;
        
        const links = footerContainer.querySelectorAll('a[href^="HTML/"], a[href^="site-helpers/"]');
        links.forEach(link => {
          let href = link.getAttribute('href');
          if (!href) return;
          
          if (isInHtmlFolder) {
            // Inside HTML folder: adjust paths relative to HTML folder root
            if (href.startsWith('HTML/')) {
              // Strip 'HTML/' prefix and add relative path if needed
              const relativePath = href.substring(5); // Remove 'HTML/'
              link.href = (depthInHtml > 0 ? '../'.repeat(depthInHtml) : '') + relativePath;
            } else if (href.startsWith('site-helpers/')) {
              // Go up to root first, then into site-helpers
              link.href = (depthInHtml > 0 ? '../'.repeat(depthInHtml) : '') + '../' + href;
            }
          } else {
            // Outside HTML folder: use prefix as before
            link.href = prefix + href;
          }
        });
      })
      .catch(error => console.error('Error loading footer:', error));
  }
}

// Load footer when DOM is ready
document.addEventListener('DOMContentLoaded', loadFooter);
