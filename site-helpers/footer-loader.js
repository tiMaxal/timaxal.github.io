// Footer loader - dynamically loads footer.html into pages
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
    if (pathLower.includes('/varhns/fishinghowto/') || 
        pathLower.includes('/varhns/aud/') || 
        pathLower.includes('/varhns/fotografi/')) {
      depth = 2;
    }
    // Check for 1-level deep folders
    else if (pathLower.includes('/aboutlife/') || 
             pathLower.includes('/sellhns/') || 
             pathLower.includes('/site-helpers/') || 
             pathLower.includes('/software/') || 
             pathLower.includes('/varhns/')) {
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
    const footerHTML = `<div class="footer">
  <p>
    <a href="https://hns.au" target="_blank">
      <img src="${imgPrefix}hnsau_blak-H-trans-bak+gg-centre_60x60.webp" alt="Handshake Australia" height="50" width="50" class="footer-logo">
    </a>
  </p>
  <p style="margin-top: 15px;">
    <a href="https://discord.gg/uKV5yKyBHG" target="_blank">
      <img src="${imgPrefix}MaxPixel.Logo-Discord-6062232.CC0.png" alt="Handshake Australia Community Discord" height="20" width="20">
    </a>
    <a href="https://www.facebook.com/people/HNS-AU/100086556653400/" target="_blank">
      <img src="${imgPrefix}fb-web.svg" alt="HNSau@fb.com" height="20" width="20">
    </a>
    <a href="https://twitter.com/tiMaxal" target="_blank">
      <img src="${imgPrefix}Twitter.svg" alt="@tiMaxal" height="20" width="20">
    </a>
  </p>
  <h6>[a <a href="https://timax.al/" target="_blank">tiMaxal</a> enterprises offering]</h6>
</div>`;
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
