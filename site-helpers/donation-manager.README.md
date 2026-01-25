# Donation Page Manager

A comprehensive CLI and GUI tool for managing payment options on the tiMaxal donation page.

## Features

- ✨ **Easy Management**: Add, update, or remove payment methods with simple commands
- 🖥️ **GUI Interface**: User-friendly graphical interface for visual management
- 💻 **CLI Support**: Command-line interface for scripting and automation
- 🔄 **Auto-Generation**: Automatically regenerates the HTML page after changes
- 📝 **JSON Configuration**: Human-readable configuration file for manual editing

## Installation

No installation required! Just ensure Python 3.6+ is installed.

## Quick Start

### GUI Mode (Recommended)

Simply run the script without arguments:

```bash
python donation-manager.py
```

This launches a tabbed GUI interface where you can:
- View all payment methods
- Add new cryptocurrencies
- Remove payment methods
- Generate the HTML file

### CLI Mode

Use command-line flags for scripting or quick changes:

```bash
python donation-manager.py --cli --list
```

## CLI Usage Examples

### List All Payment Methods

```bash
python donation-manager.py --list
```

### Add a Cryptocurrency

```bash
# With crypto domain
python donation-manager.py --add-crypto "Solana (SOL)" "◎" "SolAddressHere123..." --domain "timaxal.crypto"

# With handle/username
python donation-manager.py --add-crypto "Handshake (HNS)" "🤝" "hs1q..." --handle "@timaxal.shakestation"

# Basic (address only)
python donation-manager.py --add-crypto "Litecoin (LTC)" "Ł" "LTC_address_here"
```

### Add a Traditional Payment

```bash
python donation-manager.py --add-traditional "Venmo" "💸" "username@venmo" --note "US only"
```

### Update Payment Information

```bash
# Update cryptocurrency address
python donation-manager.py --update "Bitcoin (BTC)" --address "new_btc_address_here"

# Update email
python donation-manager.py --update "PayPal" --email "new_email@example.com"

# Update domain
python donation-manager.py --update "Ethereum (ETH)" --domain "newdomain.crypto"
```

### Remove a Payment Method

```bash
python donation-manager.py --remove "Litecoin (LTC)"
```

### Generate HTML File

```bash
python donation-manager.py --generate
```

This regenerates `../HTML/donate.html` from the current configuration.

## Configuration File

The tool stores payment information in `donation-config.json`:

```json
{
  "page_title": "Support tiMaxal - Donations",
  "intro_text": [
    "If you find value in my projects...",
    "Every contribution helps..."
  ],
  "traditional_payments": [
    {
      "name": "PayPal",
      "icon": "💰",
      "email": "tdw_m@outlook.com",
      "note": "Any currency accepted"
    }
  ],
  "cryptocurrencies": [
    {
      "name": "Bitcoin (BTC)",
      "icon": "₿",
      "domain": "timaxal.crypto",
      "address": "1N1udtUpYWRJ6bmSjDw1Tpi13obkT5mjss"
    }
  ]
}
```

You can also manually edit this file and run `--generate` to update the HTML.

## Payment Method Structure

### Traditional Payment

```json
{
  "name": "PayPal",
  "icon": "💰",
  "email": "email@example.com",
  "note": "Optional note text"
}
```

### Cryptocurrency

```json
{
  "name": "Bitcoin (BTC)",
  "icon": "₿",
  "address": "blockchain_address_here",
  "domain": "optional.crypto",      // optional
  "handle": "@optional.handle"       // optional
}
```

## GUI Screenshots

The GUI provides three tabs:

1. **View Payments**: See all configured payment methods
2. **Add Crypto**: Form to add new cryptocurrency options
3. **Remove Payment**: Remove existing payment methods

## Workflow

1. **Edit Configuration**: Use GUI or CLI to modify payment options
2. **Auto-Generate**: HTML is automatically regenerated after changes
3. **Preview**: Open `../HTML/donate.html` in a browser to preview
4. **Deploy**: Commit changes to your repository

## Tips

- Use emoji icons for visual appeal (₿, Ξ, 🤝, 💰, etc.)
- Include crypto domains (.crypto, .eth) for easier sending
- Add notes to traditional payments for currency/region info
- Keep addresses up-to-date by using the update command

## Troubleshooting

### GUI Won't Launch

If you get a tkinter error, use CLI mode:

```bash
python donation-manager.py --cli --list
```

### HTML Not Updating

Manually regenerate:

```bash
python donation-manager.py --generate
```

### Configuration Lost

The default configuration will be recreated if `donation-config.json` is deleted.

## File Locations

- Configuration: `site-helpers/donation-config.json`
- Generated HTML: `HTML/donate.html`
- Script: `site-helpers/donation-manager.py`

## License

Part of the tiMaxal website toolkit.
