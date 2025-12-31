// Theme switcher functionality
function initTheme() {
  const savedTheme = localStorage.getItem('siteTheme') || 'light';
  document.body.className = savedTheme === 'light' ? '' : savedTheme + '-theme';
  updateThemeButton();
}

function cycleTheme() {
  const currentTheme = localStorage.getItem('siteTheme') || 'light';
  let newTheme;
  
  if (currentTheme === 'light') {
    newTheme = 'dark';
  } else if (currentTheme === 'dark') {
    newTheme = 'black';
  } else {
    newTheme = 'light';
  }
  
  localStorage.setItem('siteTheme', newTheme);
  document.body.className = newTheme === 'light' ? '' : newTheme + '-theme';
  updateThemeButton();
}

function updateThemeButton() {
  const currentTheme = localStorage.getItem('siteTheme') || 'light';
  const button = document.getElementById('themeBtn') || document.getElementById('theme-switcher');
  if (button) {
    if (currentTheme === 'light') {
      button.textContent = '☀️ Light';
    } else if (currentTheme === 'dark') {
      button.textContent = '🌙 Dark';
    } else {
      button.textContent = '⚫ Black';
    }
  }
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', initTheme);
