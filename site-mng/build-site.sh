#!/bin/bash
# Build script for timax.al site
# Linux/Unix equivalent of build-site.bat

echo ""
echo "============================================="
echo "Building Site Navigation, Sitemap, and Pages..."
echo "============================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check command status
check_status() {
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: $1 failed!${NC}"
        exit 1
    fi
}

echo "[1/3] Building navigation menu..."
node menu-builder.js
check_status "Menu build"

echo ""
echo "[2/3] Building sitemap..."
node sitemap-builder.js
check_status "Sitemap build"

echo ""
echo "[3/3] Converting markdown to HTML..."
node md-to-html.js --all
check_status "Markdown conversion"

echo ""
echo "============================================="
echo -e "${GREEN}Build Complete!${NC}"
echo "============================================="
echo ""
echo "Generated files:"
echo "  - ../HTML/helpers/site-nav.js (navigation)"
echo "  - ../HTML/helpers/footer-loader.js (footer paths)"
echo "  - ../site-helpers/sitemap.xml (SEO sitemap)"
echo "  - ../site-helpers/site-map.html (user-facing sitemap)"
echo "  - ../HTML/*.html (pages from markdown in md-new/)"
echo ""
echo "Source files location:"
echo "  - ../site-helpers/md/menu.md (navigation structure)"
echo "  - ../site-helpers/md/site.md (sitemap pages)"
echo "  - ../site-helpers/md/md-new/*.md (page sources)"
echo ""
