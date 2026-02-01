@echo off
echo.
echo =============================================
echo Building Site Navigation, Sitemap, and Pages...
echo =============================================
echo.

echo [1/4] Building navigation menu...
node menu-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Menu build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [2/4] Building sitemap...
node sitemap-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Sitemap build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [3/4] Converting markdown to HTML...
node md-to-html.js --all
if %errorlevel% neq 0 (
    echo ERROR: Markdown conversion failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [4/4] Updating favicon links...
node favicon-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Favicon update failed!
    pause
    exit /b %errorlevel%
)

echo.
echo =============================================
echo Build Complete!
echo =============================================
echo.
echo Generated files:
echo   - ../HTML/helpers/site-nav.js (navigation)
echo   - ../HTML/helpers/footer-loader.js (footer paths)
echo   - ../site-helpers/sitemap.xml (SEO sitemap)
echo   - ../site-helpers/site-map.html (user-facing sitemap)
echo   - ../HTML/*.html (pages from markdown in md-new/)
echo   - Favicon links updated across HTML pages
echo.
echo Source files location:
echo   - ../site-helpers/md/menu.md (navigation structure)
echo   - ../site-helpers/md/site.md (sitemap pages)
echo   - ../site-helpers/md/md-new/*.md (page sources)
echo.
pause
