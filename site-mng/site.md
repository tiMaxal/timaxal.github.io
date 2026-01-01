# Site Map Configuration

This file defines all pages on the tiMaxal Hub website for sitemap.xml generation.
Edit this file to update the sitemap, then run `node sitemap-builder.js` to regenerate `sitemap.xml`.

## Format Guidelines
- Use `- [Page Title](path/to/file.html) | priority | changefreq` for each page
- Priority: 0.0 to 1.0 (1.0 = highest priority)
- Change Frequency: always, hourly, daily, weekly, monthly, yearly, never
- Lines starting with `#` are comments and will be ignored

## Your Domain
Base URL: https://timax.al

---

## Pages

### Home Page
- [tiMaxal Hub](./index.html) | 1.0 | weekly

### Main Sites
- [AboutLife - Holistic Self-Care](./aboutlife/aboutlife.html) | 0.9 | monthly
- [Software by tiMaxal](./software/software.html) | 0.9 | weekly
- [AUD Currency Converter](./varhns/aud/aud.html) | 0.8 | daily

### Content Pages - Various HNS Content
- [FishingHowTo - Basic Fishing Information](./varhns/FishingHowTo/FishingHowTo.html) | 0.7 | monthly
- [fishinGame - in-browser text-based game](./varhns/FishingHowTo/fishingame_webapp.html) | 0.6 | monthly
- [fotografi - Photography Gallery](./varhns/fotografi/fotografi.html) | 0.7 | monthly
- [CC0 Images](./varhns/fotografi/cc0img.html) | 0.6 | monthly
- [CC-BY Images](./varhns/fotografi/cc-by_img.html) | 0.6 | monthly
- [TheBlackDog - Mental Health Organization](./varhns/TheBlackDog.html) | 0.8 | monthly
- [uvau](./varhns/uvau.html) | 0.6 | monthly

### Commerce
- [Buy HNS TLDs](./sellhns/hnsell.html) | 0.8 | weekly
- [HNS Sell - Alternate Page](./sellhns/nb-sell.html) | 0.7 | weekly

### Utilities
- [Site Map](./site-helpers/site-map.html) | 0.5 | monthly
