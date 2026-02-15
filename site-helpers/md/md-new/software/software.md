---
title: Software Projects
path: software/software.html
---

# Software by tiMaxal

<style>
  .container {
    max-width: 1200px;
  }

  .intro {
    text-align: center;
    margin: 20px 0 40px 0;
    font-size: 1.1em;
  }

  .repo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
    margin: 30px 0;
  }

  .repo-card {
    border: 2px solid currentColor;
    border-radius: 8px;
    padding: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .repo-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }

  .repo-card h3 {
    font-size: 1.3em;
    margin-bottom: 10px;
  }

  .repo-card h3 a {
    color: inherit;
    text-decoration: none;
  }

  .repo-card h3 a:hover {
    text-decoration: underline;
  }

  .repo-description {
    margin: 15px 0;
    min-height: 50px;
  }

  .repo-meta {
    display: flex;
    gap: 15px;
    margin-top: 15px;
    font-size: 0.9em;
    opacity: 0.8;
  }

  .repo-language {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .language-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
  }

  .repo-stars {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .loading {
    text-align: center;
    padding: 40px;
    font-size: 1.2em;
    opacity: 0.7;
  }

  .last-updated {
    text-align: center;
    font-size: 0.9em;
    opacity: 0.6;
    margin: 20px 0;
  }

  .error-message {
    text-align: center;
    padding: 20px;
    color: #ff0000;
    background-color: rgba(255, 0, 0, 0.1);
    border-radius: 8px;
    margin: 20px 0;
  }

  .controls {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
  }

  .control-btn {
    padding: 8px 16px;
    border: 2px solid currentColor;
    border-radius: 5px;
    background-color: transparent;
    color: inherit;
    cursor: pointer;
    font-size: 0.9em;
    transition: all 0.2s ease;
  }

  .control-btn:hover {
    background-color: rgba(52, 4, 244, 0.1);
    transform: scale(1.05);
  }

  body.dark-theme .control-btn:hover {
    background-color: rgba(153, 221, 255, 0.1);
  }

  body.black-theme .control-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 30px 0 20px 0;
    border-bottom: 2px solid currentColor;
    padding-bottom: 10px;
  }

  .header-row h2 {
    margin: 0;
    border: none;
    padding: 0;
  }

  @media (max-width: 768px) {
    .repo-grid {
      grid-template-columns: 1fr;
    }

    .controls {
      flex-direction: column;
      align-items: flex-start;
    }

    .header-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
    }
  }

  .footer {
    text-align: center;
    margin-top: 50px;
    padding: 30px 20px;
    border-top: 2px solid currentColor;
  }

  .footer p {
    margin: 10px 0;
  }

  .footer img {
    margin: 0 10px;
    vertical-align: middle;
  }

  .footer h6 {
    margin-top: 20px;
    font-size: 0.9em;
  }
</style>

<div class="intro">
  <p>Open source projects and tools developed by tiMaxal, often by voding [ai vibe-coding].</p>
  <p>ALL possible care but NO responsibility taken for app efficacy. <strong>Use at own risk!</strong></p>
  <p>Explore the repositories on <a href="https://github.com/tiMaxal" target="_blank" rel="noopener">GitHub</a>.</p>
  <p class="last-updated" id="lastUpdated"></p>
</div>

<div class="header-row">
  <h2>🛠️ Original Projects</h2>
  <div class="controls">
    <button class="control-btn" id="sortBtn" onclick="toggleSort()">📅 Most Recent</button>
    <button class="control-btn" id="refreshBtn" onclick="forceRefresh()">🔄 Refresh</button>
    <a href="https://github.com/tiMaxal" target="_blank" rel="noopener" class="control-btn" style="text-decoration: none;">→ View All</a>
  </div>
</div>

<div class="repo-grid" id="repoGrid">
  <div class="loading">Loading repositories...</div>
</div>

<script src="../helpers/software-repos.js"></script>