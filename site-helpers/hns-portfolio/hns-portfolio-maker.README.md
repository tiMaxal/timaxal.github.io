# HNS Portfolio Maker for timax.al - Enhanced Version

**Updated:** January 6, 2026

## Overview

CLI tool for generating HNS portfolio HTML pages with full timax.al site integration. Supports 4+ CSV formats, advanced filtering, sorting, and contact information display.

## Key Features

### ✅ **Expanded CSV Format Support**
- **Namebase**: TLD exports & Transactions
- **HSD Sales Truth**: Complete domain inventory from Handshake SD
- **Bob Wallet**: TLD lists (processed or original single-column)
- **Firewallet**: Domain exports

### ✅ **Marketplace Linking**
- Namebase domains → `namebase.io/domains/{name}`
- HSD/Bob/Firewallet → Contact info display (no marketplace link)

### ✅ **Contact Information**
- Price display with 💰 icon
- Email with 📧 copy-to-clipboard button
- Auto-append email for domains with price: `user+domain@gmail.com`
- **Requirement**: Bob/FW/HSD domains MUST have email or price to be displayed

### ✅ **Advanced Search & Filter**
- Text search (domain names)
- Price range (min/max)
- Tag filtering (3D-7D, 3L-5L, 3C-4C, PUNY_IDNA, PUNY_ALT, language tags)

### ✅ **Sort Options** (5 modes)
1. Random
2. Alphabetical A-Z ▲
3. Alphabetical Z-A ▼
4. Price Low-High ▲
5. Price High-Low ▼

### ✅ **Site Integration**
- Top marketplace links (randomized on load): Bob Wallet, Namebase, Fingertip, **FireWallet**
- Links to site-nav.css, theme-switcher.js, footer-loader.js, site-nav.js
- 3-way theme switcher: Light (#ccffff) → Dark (#003366) → Black (#000000)
- Credits section (themed with page) above footer
- Footer loaded via external container

### ✅ **CLI & Settings File Support**
- Command-line arguments for all options
- JSON settings file for batch processing
- Help system with examples
- Auto-save settings option

---

## Usage

### Basic Usage
```bash
# Process single file
python hns-portfolio-maker.py domains.csv

# Process multiple files with title
python hns-portfolio-maker.py -t "My HNS Domains" file1.csv file2.csv

# With auto-email for Bob/FW domains
python hns-portfolio-maker.py -e user+@gmail.com bob-domains.csv
```

### Command-Line Options
```
-h, --help              Show help message
-s, --settings FILE     Use settings file (default: portfolio-settings.json)
-o, --output FILE       Output HTML filename (default: portfolio.html)
-t, --title TITLE       Page title (default: HNS Portfolio)
-e, --email EMAIL       Auto-append email (format: user@gmail.com or user+@gmail.com)
-c, --credits FILE      Credits HTML file (e.g., html/credits.html)
--save-settings         Save current settings to file
--create-settings       Create example settings file
```

### Settings File
```bash
# Create example settings file
python hns-portfolio-maker.py --create-settings

# Use settings file
python hns-portfolio-maker.py -s my-settings.json
```

**Example settings.json:**
```json
{
  "email": "yourname+@gmail.com",
  "output_filename": "my-portfolio.html",
  "title": "HNS Domain Portfolio",
  "credits_file": "html/credits.html",
  "include_descriptions": false,
  "all": false,
  "csv_files": [
    "csv-s/csv-nb/csv_nb-tld/Namebase-domains-export.csv",
    "csv-s/csv-hsd/hns_hsd_sales_truth.csv",
    "csv-s"
  ]
}
```

**Settings File Options:**
- `email`: Email template for Bob/FW domains (use `+` for per-domain variation)
- `output_filename`: Output HTML filename
- `title`: Page title
- `credits_file`: Path to credits HTML file
- `include_descriptions`: `true` = show descript-IDNA and translate-IDNA fields
- **`all`**: `true` = include ALL domains; `false` = only domains with price (for Bob/FW/HSD sources)
- **`csv_files`**: Array of CSV file paths **OR directories** (searched recursively for `*.csv` files)

---

## CSV Requirements

### Namebase TLD
- **Required columns**: `name`
- **Optional**: `unicode`, `tags`, `descript-IDNA`, `email`, `price`
- **Links to**: Namebase marketplace

### Namebase Transactions
- **Required columns**: `extra.domain`
- **Optional**: `unicode`, `tags`
- **Links to**: Namebase marketplace

### HSD Sales Truth
- **Required columns**: `domains`, `wallet_id`, `ownership_status`
- **Optional**: `unicode`, `tags`, `email`, `price`, `descript-IDNA`, `translate-IDNA`
- **Contact display only** (no marketplace link)

### Bob Wallet TLD
- **Format 1**: Single column (no header) with domain names
- **Format 2**: `domains` column with optional `unicode`, `tags`
- **Required**: `email` OR `price` column (or use `--email` flag)
- **Contact display only** (no marketplace link)

### Firewallet
- **Required columns**: First column (name), `expiry`
- **Optional**: `unicode`, `tags`
- **Required**: `email` OR `price` column (or use `--email` flag)
- **Contact display only** (no marketplace link)



---

## Output Location

Files are saved to: `../HTML/sellhns/` (relative to script location)

For example:
```
site-helpers/hns-portfolio-maker.py
HTML/sellhns/portfolio.html  ← Output location
```

---

## Examples

### Process Namebase & HSD CSVs
```bash
python hns-portfolio-maker.py \
  -t "timax.al HNS Portfolio" \
  -o timax-hns.html \
  csv-nb/nb-export.csv \
  csv-hsd/hns_hsd_sales_truth.csv
```

### Process Bob Wallet with Auto-Email
```bash
python hns-portfolio-maker.py \
  -e tim+@gmail.com \
  -t "Bob Wallet Domains" \
  csv-bob/bob-domains.csv
```

### Process Firewallet with Credits
```bash
python hns-portfolio-maker.py \
  -e contact+@timax.al \
  -c html/credits.html \
  -t "Firewallet Portfolio" \
  csv-fw/fw-export.csv
```

### Batch Processing with Settings
```bash
# Create settings file
python hns-portfolio-maker.py --create-settings

# Edit portfolio-settings.json, then:
python hns-portfolio-maker.py -s portfolio-settings.json
```

---

## Troubleshooting

### "No domains found in CSV files!"
**Possible causes:**
- Bob/Firewallet/HSD CSVs missing `email` or `price` columns
- Invalid CSV format

**Solution:**
```bash
# For Bob/FW: Add --email flag
python hns-portfolio-maker.py -e user+@gmail.com bob-domains.csv
```

### Bob/Firewallet/HSD Domains Not Showing
Bob, Firewallet, and HSD domains **require** either:
1. `email` column in CSV, OR
2. `price` column in CSV, OR
3. `--email` CLI flag with price column

Without contact info, these domains are skipped (no marketplace link available).

### Credits Not Showing
- Check credits file path (relative to script or absolute)
- File should contain HTML snippet with inline styles
- Example: `html/credits.html`

---

## Comparison: hns-portfolio-maker.py vs HNSell Tab 3

| Feature | hns-portfolio-maker.py | HNSell Tab 3 |
|---------|------------------------|--------------|
| **Interface** | CLI, scriptable | GUI |
| **CSV Formats** | nb-tld, nb-tr, hsd, bob-tld, fw | Varies |
| **Price/Email** | ✅ Full support | ✅ Full support |
| **Auto-Email** | ✅ CLI flag | ✅ GUI field |
| **Search/Filter** | ✅ Text, price, tags | ✅ Text, price |
| **Sort** | ✅ 5 modes | ✅ 5 modes |
| **Theme** | ✅ timax.al 3-way | ✅ 3 options |
| **Site Integration** | ✅ External CSS/JS | ❌ Self-contained |
| **Settings File** | ✅ JSON | ❌ None |
| **Help** | ✅ CLI help | ✅ GUI help |
| **Output Path** | ✅ Configurable | ❌ Script dir only |
| **Batch Mode** | ✅ Via settings | ❌ GUI only |

---

## Dependencies

```bash
pip install pandas
```

---

## Credits

- Based on punytag tools by [@i1li](https://github.com/i1li/punytag)
- Enhanced for timax.al by timax (2026)

---

## Version History

- **v2.0** (2026-01-06): Enhanced version
  - Added Bob Wallet & Firewallet support
  - Advanced search/filter (price, tags)
  - Sort controls (5 modes)
  - Settings file support
  - CLI arguments
  - Credits section integration
  - Auto-email feature
  - Marketplace links randomization

- **v1.0**: Initial timax.al version
  - Basic Namebase/HSD support
  - 3-way theme switcher
  - Site integration
