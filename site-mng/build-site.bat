@echo off
REM Ensure node is available (check PATH, then common install locations)
where node >nul 2>nul
if %errorlevel% neq 0 (
    for %%P in (
        "C:\Program Files\nodejs"
        "C:\Program Files (x86)\nodejs"
    ) do (
        if exist "%%~P\node.exe" (
            set "PATH=%%~P;%PATH%"
            goto :NODE_FOUND
        )
    )
    for /d %%P in ("C:\Users\Public\node-*-win-x64") do (
        if exist "%%~P\node.exe" (
            set "PATH=%%~P;%PATH%"
            goto :NODE_FOUND
        )
    )
)
:NODE_FOUND
echo.
echo =============================================
echo Building Site Navigation, Sitemap, and Pages...
echo =============================================
echo.

echo [1/4] Normalising helper paths and favicon links...
node helper-paths-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Helper paths/favicon build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [2/4] Building navigation menu...
node menu-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Menu build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [3/4] Building sitemap...
node sitemap-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Sitemap build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [4/4] Converting markdown to HTML...
node md-to-html.js --all
if %errorlevel% neq 0 (
    echo ERROR: Markdown conversion failed!
    pause
    exit /b %errorlevel%
)

echo.
echo =============================================
echo Build Complete!
echo =============================================
echo.
echo Generated files:
echo   - Helper paths normalised (site-nav.css/js, theme-switcher.js, footer-loader.js)
echo   - Favicon links normalised across HTML pages
echo   - ../HTML/helpers/site-nav.js (navigation)
echo   - ../HTML/helpers/footer-loader.js (footer paths)
echo   - ../site-helpers/sitemap.xml (SEO sitemap)
echo   - ../site-helpers/site-map.html (user-facing sitemap)
echo   - ../HTML/*.html (pages from markdown in md-new/)
echo.
echo Source files location:
echo   - ../site-helpers/md/menu.md (navigation structure)
echo   - ../site-helpers/md/site.md (sitemap pages)
echo   - ../site-helpers/md/md-new/*.md (page sources)
echo.
pause
