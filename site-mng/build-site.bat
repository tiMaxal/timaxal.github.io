@echo off
echo.
echo =============================================
echo Building Site Navigation and Sitemap...
echo =============================================
echo.

echo [1/2] Building navigation menu...
node menu-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Menu build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [2/2] Building sitemap...
node sitemap-builder.js
if %errorlevel% neq 0 (
    echo ERROR: Sitemap build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo =============================================
echo Build Complete!
echo =============================================
echo.
echo Generated files:
echo   - ../site-helpers/site-nav.js (navigation)
echo   - ../site-helpers/footer-loader.js (footer paths)
echo   - ../site-helpers/sitemap.xml (SEO sitemap)
echo   - ../site-helpers/site-map.html (user-facing sitemap)
echo.
pause
