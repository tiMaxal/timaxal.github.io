// GitHub API configuration
const GITHUB_USERNAME = 'tiMaxal';
const CACHE_KEY = 'github_repos_cache';
const CACHE_DURATION = 86400000; // 24 hours in milliseconds
const MIN_REFRESH_INTERVAL = 3600000; // 1 hour minimum for forced refresh
const LAST_REFRESH_KEY = 'last_manual_refresh';

// Repositories to ignore
const IGNORE_REPOS = [
  'hello-world',
  'timaxal.github.io',
  'timaskal.github.io'
];

// Sort state
let currentSort = 'recent'; // 'recent' or 'alpha'

// Language colors from GitHub
const languageColors = {
  'Python': '#3572A5',
  'JavaScript': '#f1e05a',
  'HTML': '#e34c26',
  'CSS': '#563d7c',
  'TypeScript': '#2b7489',
  'Java': '#b07219',
  'C': '#555555',
  'C++': '#f34b7d',
  'C#': '#178600',
  'PHP': '#4F5D95',
  'Ruby': '#701516',
  'Go': '#00ADD8',
  'Rust': '#dea584',
  'Shell': '#89e051',
  'Vue': '#41b883'
};

// Check if cached data is still valid
function getCachedData() {
  try {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      const { data, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp < CACHE_DURATION) {
        return data;
      }
    }
  } catch (e) {
    console.error('Cache read error:', e);
  }
  return null;
}

// Save data to cache
function cacheData(data) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({
      data: data,
      timestamp: Date.now()
    }));
  } catch (e) {
    console.error('Cache write error:', e);
  }
}

// Fetch repositories from GitHub API
async function fetchRepositories() {
  try {
    const response = await fetch(`https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=100`);

    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.status}`);
    }

    const repos = await response.json();

    // Filter non-forked repos and ignored repos
    const originalRepos = repos
      .filter(repo => !repo.fork && !IGNORE_REPOS.includes(repo.name))
      .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));

    return originalRepos;
  } catch (error) {
    console.error('Error fetching repositories:', error);
    throw error;
  }
}

// Create repo card HTML
function createRepoCard(repo) {
  const languageColor = languageColors[repo.language] || '#cccccc';
  const stars = repo.stargazers_count > 0 ? `<span class="repo-stars">⭐ ${repo.stargazers_count}</span>` : '';
  const license = repo.license ? `<span>${repo.license.spdx_id}</span>` : '';
  const description = repo.description || 'No description available';
  const language = repo.language || 'Unknown';

  return `
    <div class="repo-card">
      <h3><a href="${repo.html_url}" target="_blank" rel="noopener">${repo.name}</a></h3>
      <div class="repo-description">${description}</div>
      <div class="repo-meta">
        <span class="repo-language">
          <span class="language-dot" style="background-color: ${languageColor};"></span>
          ${language}
        </span>
        ${stars}
        ${license}
      </div>
    </div>
  `;
}

// Sort repositories
function sortRepos(repos, sortType) {
  const sorted = [...repos];
  if (sortType === 'alpha') {
    sorted.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
  } else {
    sorted.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
  }
  return sorted;
}

// Toggle sort
function toggleSort() {
  currentSort = currentSort === 'recent' ? 'alpha' : 'recent';
  const sortBtn = document.getElementById('sortBtn');
  sortBtn.textContent = currentSort === 'recent' ? '📅 Most Recent' : '🔤 Alphabetical';

  const cachedRepos = getCachedData();
  if (cachedRepos) {
    updateRepoGrid(sortRepos(cachedRepos, currentSort));
  }
}

// Force refresh with 1-hour minimum interval
async function forceRefresh() {
  const lastRefresh = localStorage.getItem(LAST_REFRESH_KEY);
  const now = Date.now();

  if (lastRefresh && (now - parseInt(lastRefresh, 10)) < MIN_REFRESH_INTERVAL) {
    const remainingTime = Math.ceil((MIN_REFRESH_INTERVAL - (now - parseInt(lastRefresh, 10))) / 60000);
    alert(`Please wait ${remainingTime} more minute(s) before refreshing again.`);
    return;
  }

  const refreshBtn = document.getElementById('refreshBtn');
  refreshBtn.disabled = true;
  refreshBtn.textContent = '⏳ Refreshing...';

  try {
    const repos = await fetchRepositories();
    updateRepoGrid(sortRepos(repos, currentSort));
    cacheData(repos);
    localStorage.setItem(LAST_REFRESH_KEY, now.toString());
  } catch (error) {
    showError('Failed to refresh repositories.');
  } finally {
    refreshBtn.disabled = false;
    refreshBtn.textContent = '🔄 Refresh';
  }
}

// Update the repository grid
function updateRepoGrid(repos) {
  const grid = document.getElementById('repoGrid');

  if (repos && repos.length > 0) {
    const sortedRepos = sortRepos(repos, currentSort);
    grid.innerHTML = sortedRepos.map(repo => createRepoCard(repo)).join('');

    // Update last updated timestamp
    const lastUpdated = document.getElementById('lastUpdated');
    lastUpdated.textContent = `Last updated: ${new Date().toLocaleString()}`;
  } else {
    grid.innerHTML = '<div class="error-message">No repositories found.</div>';
  }
}

// Show error message
function showError(message) {
  const grid = document.getElementById('repoGrid');
  grid.innerHTML = `<div class="error-message">${message}</div>`;
}

// Main initialization function
async function initializeRepos() {
  // Try to load from cache first
  const cachedRepos = getCachedData();

  if (cachedRepos) {
    updateRepoGrid(cachedRepos);

    // Update last updated time from cache
    const cached = JSON.parse(localStorage.getItem(CACHE_KEY));
    const lastUpdated = document.getElementById('lastUpdated');
    lastUpdated.textContent = `Last updated: ${new Date(cached.timestamp).toLocaleString()} (cached)`;
  }

  // Fetch fresh data in the background
  try {
    const repos = await fetchRepositories();
    updateRepoGrid(repos);
    cacheData(repos);
  } catch (error) {
    // If we have cached data, keep using it
    if (!cachedRepos) {
      showError('Failed to load repositories. Please try again later.');
    }
  }
}

// Auto-refresh daily
setInterval(initializeRepos, CACHE_DURATION);

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeRepos);
