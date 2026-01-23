/**
 * Handshake Inline Button
 * Adds a discreet "HNS ↗" button next to links that have Handshake versions.
 * Non-intrusive approach that preserves normal site navigation.
 * 
 * Usage: <script src="../../site-helpers/i2h/handshake-button.js" 
 *                domain="aboutlife" 
 *                protocol="http"
 *                linkSelector=".header h1 a, .site-link h3 a"></script>
 * 
 * Or for single link: <a href="page.html" class="has-hns" data-hns-domain="aboutlife" data-hns-protocol="http">Link</a>
 */
(function() {
  const targetDomain = document.currentScript.getAttribute('domain');
  const targetProtocol = document.currentScript.getAttribute('protocol') || 'https';
  const linkSelector = document.currentScript.getAttribute('linkSelector');
  
  // Check if we're not already on HNS domain
  if (location.hostname === targetDomain) {
    console.log('Already on HNS domain - buttons not shown');
    return;
  }
  
  // Function to create HNS button
  function createHNSButton(hnsUrl, inline = true) {
    const button = document.createElement('a');
    button.href = hnsUrl;
    button.target = '_blank';
    button.rel = 'noopener noreferrer';
    button.className = 'hns-button';
    button.innerHTML = '🌐 HNS';
    button.title = 'Open Handshake version in new tab';
    
    // Inline styling for consistent appearance
    button.style.cssText = `
      display: inline-block;
      margin-left: ${inline ? '8px' : '0'};
      padding: 2px 8px;
      font-size: 0.75em;
      font-weight: normal;
      background: rgba(52, 4, 244, 0.15);
      color: #3404f4;
      border: 1px solid rgba(52, 4, 244, 0.3);
      border-radius: 4px;
      text-decoration: none;
      transition: all 0.2s ease;
      vertical-align: middle;
      white-space: nowrap;
    `;
    
    // Theme-aware styling
    function updateButtonTheme() {
      const currentTheme = localStorage.getItem('siteTheme') || 'light';
      
      if (currentTheme === 'dark') {
        button.style.background = 'rgba(153, 221, 255, 0.15)';
        button.style.color = '#99ddff';
        button.style.borderColor = 'rgba(153, 221, 255, 0.3)';
      } else if (currentTheme === 'black') {
        button.style.background = 'rgba(255, 255, 255, 0.15)';
        button.style.color = '#ffffff';
        button.style.borderColor = 'rgba(255, 255, 255, 0.3)';
      } else {
        button.style.background = 'rgba(52, 4, 244, 0.15)';
        button.style.color = '#3404f4';
        button.style.borderColor = 'rgba(52, 4, 244, 0.3)';
      }
    }
    
    // Hover effects
    button.addEventListener('mouseenter', function() {
      const currentTheme = localStorage.getItem('siteTheme') || 'light';
      if (currentTheme === 'dark') {
        this.style.background = 'rgba(153, 221, 255, 0.3)';
      } else if (currentTheme === 'black') {
        this.style.background = 'rgba(255, 255, 255, 0.3)';
      } else {
        this.style.background = 'rgba(52, 4, 244, 0.25)';
      }
      this.style.transform = 'scale(1.05)';
    });
    
    button.addEventListener('mouseleave', function() {
      updateButtonTheme();
      this.style.transform = 'scale(1)';
    });
    
    updateButtonTheme();
    
    // Listen for theme changes
    if (document.body) {
      const themeObserver = new MutationObserver(updateButtonTheme);
      themeObserver.observe(document.body, {
        attributes: true,
        attributeFilter: ['class']
      });
    }
    
    return button;
  }
  
  // Function to add buttons to specific links
  function addButtonsToLinks() {
    if (!linkSelector) return;
    
    const links = document.querySelectorAll(linkSelector);
    links.forEach(link => {
      // Skip if button already added
      if (link.nextElementSibling && link.nextElementSibling.classList.contains('hns-button')) {
        return;
      }
      
      const hnsUrl = `${targetProtocol}://${targetDomain}${location.pathname}`;
      const button = createHNSButton(hnsUrl, true);
      
      // Insert button after the link
      link.parentNode.insertBefore(button, link.nextSibling);
    });
  }
  
  // Function to enhance links with data attributes
  function enhanceDataLinks() {
    const dataLinks = document.querySelectorAll('[data-hns-domain]');
    dataLinks.forEach(link => {
      // Skip if button already added
      if (link.nextElementSibling && link.nextElementSibling.classList.contains('hns-button')) {
        return;
      }
      
      const hnsDomain = link.getAttribute('data-hns-domain');
      const hnsProtocol = link.getAttribute('data-hns-protocol') || 'https';
      const hnsPath = link.getAttribute('data-hns-path') || link.getAttribute('href') || '';
      
      const hnsUrl = `${hnsProtocol}://${hnsDomain}${hnsPath}`;
      const button = createHNSButton(hnsUrl, true);
      
      // Insert button after the link
      link.parentNode.insertBefore(button, link.nextSibling);
    });
  }
  
  // Initialize when DOM is ready
  function initialize() {
    if (document.body) {
      if (linkSelector) {
        addButtonsToLinks();
      }
      enhanceDataLinks();
    }
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
})();
