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
    const footerHTML = `<div class="footer"><p>Footer content not found</p></div>`;
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
