# Pull Request: testing → main

## Summary

Major site restructure with enhanced tooling, markdown workflow, and content additions.

## Key Changes

### Site Structure

- **Reorganized directory layout**: Moved HTML content to `HTML/` directory
- **Helper consolidation**: Moved build tools to `site-helpers/` and `site-mng/`
- **Image assets**: Reorganized to `HTML/imgs/` with proper subdirectories

### New Features

- **Markdown workflow**: Implemented `*.md` → HTML conversion system with build scripts
- **Site navigation**: Added dynamic menu builder, theme switcher, footer loader
- **HNS Portfolio Maker**: Enhanced tool with "buy now only" option
- **Sitemap**: Added XML sitemap and site map HTML page

### Content Additions

- **Software page**: New page showcasing software projects
- **Fishing game**: Added interactive fishing web app
- **HNS merchandising**: Enhanced HNS domain selling pages with logos/buttons
- **Donation manager**: Python tool for managing site donations

### Documentation

- Added comprehensive READMEs for portfolio maker, donation manager
- Created `MARKDOWN-WORKFLOW.md`, `SITE-MANAGEMENT.md`, `QUICK-REFERENCE.md`
- Documented fixes and updates in `FIXES-SUMMARY.md`, `UPDATES-2026-01-24.md`

### Build System

- `build-site.bat` (Windows) and `build-site.sh` (Linux) for automated builds
- `md-to-html.js`, `menu-builder.js`, `sitemap-builder.js` for site generation
- Node.js dependencies: added `marked` package

### Technical Improvements

- Improved footer with dynamic loading
- Enhanced theme switcher functionality
- Better Handshake domain integration scripts
- Low bandwidth options documented

## File Stats

- **409 files changed**: 37,031 additions, 911 deletions
- New binary assets: ~200+ image files (CC0/CC-BY photography, HNS logos)
- New node_modules: marked package + dependencies

## Commits (13)

Latest commits in chronological order:

1. Modernize site theme + menu; add software page; add sitemap
2. Adapt home button colors
3. Move construction files to /site-mng and helpers to /site-helpers
4. Add fishing game; fix index.html layout
5. Reorganize: HTML/ directory + site-helpers/ directory
6. Update docs for new HTML/ structure
7. Restructure portfolio tooling to hns-portfolio/
8. Clean up hns-portfolio directory (.gitignore, remove backups)
9. Update HNSell, add HNS buttons/logos + footer/donate features
10. Implement markdown editing workflow + build-site.sh
11. Update footer sitemap link to dynamic
12. Add 'buy now only' option to hns-portfolio-maker
13. Archive ISSUES_TO_FIX.md

---
*Generated: 2026-01-25*
