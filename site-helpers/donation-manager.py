#!/usr/bin/env python3
"""
Donation Page Manager
====================

A CLI and GUI tool for managing payment options on the tiMaxal donation page.

This script allows you to:
- Add new payment methods
- Update existing payment information
- Remove payment methods
- Preview the donation page
- Generate the HTML automatically

Usage:
    python donation-manager.py          # Launch GUI
    python donation-manager.py --cli    # Use CLI mode
    python donation-manager.py --add "Payment Name" "address" "domain"
    python donation-manager.py --update "Payment Name" --address "new_address"
    python donation-manager.py --remove "Payment Name"
    python donation-manager.py --list   # List all payment methods
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Configuration file path
SCRIPT_DIR = Path(__file__).parent.absolute()
CONFIG_FILE = SCRIPT_DIR / "donation-config.json"
DONATE_HTML = SCRIPT_DIR.parent / "HTML" / "donate.html"

# Default configuration
DEFAULT_CONFIG = {
    "page_title": "Support tiMaxal - Donations",
    "intro_text": [
        "If you find value in my projects, software, or content, consider supporting my work through a donation.",
        "Every contribution helps keep the projects alive and enables me to create more!"
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
            "name": "BASE",
            "icon": "🔷",
            "domain": "timaxal.crypto",
            "address": "0xC56aC83cD58EDd302379f39d72131e83e36B541b"
        },
        {
            "name": "Bitcoin (BTC)",
            "icon": "₿",
            "domain": "timaxal.crypto",
            "address": "1N1udtUpYWRJ6bmSjDw1Tpi13obkT5mjss"
        },
        {
            "name": "Ethereum (ETH)",
            "icon": "Ξ",
            "domain": "timaxal.crypto",
            "address": "0xC56aC83cD58EDd302379f39d72131e83e36B541b"
        },
        {
            "name": "Handshake (HNS)",
            "icon": "🤝",
            "handle": "@timaxal.shakestation",
            "address": "hs1qwwsfgyxxvgq6k4qwcr0syyqss2c3ydxq4p3mml"
        },
        {
            "name": "Polygon (MATIC)",
            "icon": "🟣",
            "domain": "timaxal.crypto",
            "address": "0xC56aC83cD58EDd302379f39d72131e83e36B541b"
        }
    ]
}


class DonationManager:
    """Manages donation page configuration and HTML generation."""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from JSON file or create default."""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Optional[Dict] = None):
        """Save configuration to JSON file."""
        if config is None:
            config = self.config
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def add_crypto(self, name: str, icon: str, address: str, domain: Optional[str] = None, 
                   handle: Optional[str] = None):
        """Add a new cryptocurrency payment method."""
        crypto = {
            "name": name,
            "icon": icon,
            "address": address
        }
        if domain:
            crypto["domain"] = domain
        if handle:
            crypto["handle"] = handle
        
        self.config["cryptocurrencies"].append(crypto)
        self.save_config()
        print(f"✓ Added {name}")
    
    def add_traditional(self, name: str, icon: str, email: str, note: Optional[str] = None):
        """Add a new traditional payment method."""
        payment = {
            "name": name,
            "icon": icon,
            "email": email
        }
        if note:
            payment["note"] = note
        
        self.config["traditional_payments"].append(payment)
        self.save_config()
        print(f"✓ Added {name}")
    
    def remove_payment(self, name: str) -> bool:
        """Remove a payment method by name."""
        # Check traditional payments
        for i, payment in enumerate(self.config["traditional_payments"]):
            if payment["name"].lower() == name.lower():
                self.config["traditional_payments"].pop(i)
                self.save_config()
                print(f"✓ Removed {name}")
                return True
        
        # Check cryptocurrencies
        for i, crypto in enumerate(self.config["cryptocurrencies"]):
            if crypto["name"].lower() == name.lower():
                self.config["cryptocurrencies"].pop(i)
                self.save_config()
                print(f"✓ Removed {name}")
                return True
        
        print(f"✗ Payment method '{name}' not found")
        return False
    
    def update_payment(self, name: str, **kwargs):
        """Update payment method details."""
        # Check traditional payments
        for payment in self.config["traditional_payments"]:
            if payment["name"].lower() == name.lower():
                payment.update(kwargs)
                self.save_config()
                print(f"✓ Updated {name}")
                return True
        
        # Check cryptocurrencies
        for crypto in self.config["cryptocurrencies"]:
            if crypto["name"].lower() == name.lower():
                crypto.update(kwargs)
                self.save_config()
                print(f"✓ Updated {name}")
                return True
        
        print(f"✗ Payment method '{name}' not found")
        return False
    
    def list_payments(self):
        """List all payment methods."""
        print("\n=== Traditional Payments ===")
        for payment in self.config["traditional_payments"]:
            print(f"  {payment['icon']} {payment['name']}: {payment.get('email', 'N/A')}")
        
        print("\n=== Cryptocurrencies ===")
        for crypto in self.config["cryptocurrencies"]:
            print(f"  {crypto['icon']} {crypto['name']}")
            if 'domain' in crypto:
                print(f"    Domain: {crypto['domain']}")
            if 'handle' in crypto:
                print(f"    Handle: {crypto['handle']}")
            print(f"    Address: {crypto['address']}")
        print()
    
    def generate_html(self) -> str:
        """Generate the donation page HTML from configuration."""
        # Read the current HTML template structure
        html_parts = []
        
        # HTML Header
        html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''' + self.config['page_title'] + '''</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background-color: #ccffff;
            color: #3404f4;
            padding: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        body.dark-theme {
            background-color: #003366;
            color: #99ddff;
        }

        body.black-theme {
            background-color: #000000;
            color: #ffffff;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        h1 {
            font-size: 2.5em;
            margin: 30px 0;
            text-align: center;
        }

        .intro {
            text-align: center;
            margin: 20px 0 40px 0;
            font-size: 1.1em;
            padding: 0 20px;
        }

        .payment-section {
            margin: 40px 0;
        }

        .payment-section h2 {
            font-size: 1.5em;
            margin-bottom: 25px;
            border-bottom: 2px solid currentColor;
            padding-bottom: 10px;
        }

        .payment-options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .payment-card {
            border: 2px solid currentColor;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.05);
        }

        .payment-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }

        body.dark-theme .payment-card {
            background: rgba(255, 255, 255, 0.03);
        }

        body.black-theme .payment-card {
            background: rgba(255, 255, 255, 0.02);
        }

        .payment-card h3 {
            font-size: 1.4em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .payment-card .currency-icon {
            font-size: 1.2em;
            font-weight: bold;
        }

        .payment-info {
            margin: 15px 0;
        }

        .payment-label {
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.8;
        }

        .payment-value {
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            word-break: break-all;
            padding: 10px;
            background: rgba(0, 0, 0, 0.1);
            border-radius: 6px;
            margin-bottom: 10px;
        }

        body.dark-theme .payment-value {
            background: rgba(255, 255, 255, 0.1);
        }

        body.black-theme .payment-value {
            background: rgba(255, 255, 255, 0.15);
        }

        .copy-btn {
            background-color: rgba(52, 4, 244, 0.8);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s ease;
        }

        .copy-btn:hover {
            background-color: rgba(52, 4, 244, 1);
            transform: scale(1.05);
        }

        body.dark-theme .copy-btn {
            background-color: rgba(153, 221, 255, 0.8);
            color: #003366;
        }

        body.dark-theme .copy-btn:hover {
            background-color: rgba(153, 221, 255, 1);
        }

        body.black-theme .copy-btn {
            background-color: rgba(102, 187, 255, 0.8);
            color: #000;
        }

        body.black-theme .copy-btn:hover {
            background-color: rgba(102, 187, 255, 1);
        }

        .copy-btn.copied {
            background-color: #28a745;
        }

        a:link { color: #0000ee; }
        a:visited { color: #551a8b; }
        a:active { color: #ee0000; }
        a:hover { 
            color: #3404f4;
            text-decoration: underline;
        }

        body.dark-theme a:link { color: #66bbff; }
        body.dark-theme a:visited { color: #9988ff; }
        body.dark-theme a:hover { color: #99ddff; }

        body.black-theme a:link { color: #66bbff; }
        body.black-theme a:visited { color: #9999ff; }
        body.black-theme a:hover { color: #ffffff; }

        .theme-switcher {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background-color: rgba(52, 4, 244, 0.8);
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 0.9em;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            z-index: 1000;
        }

        .theme-switcher:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        }

        body.dark-theme .theme-switcher {
            background-color: rgba(153, 221, 255, 0.8);
            color: #003366;
        }

        body.black-theme .theme-switcher {
            background-color: rgba(255, 255, 255, 0.8);
            color: #000000;
        }

        .back-home {
            text-align: center;
            margin: 40px 0;
            font-size: 1.1em;
        }

        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid currentColor;
            opacity: 0.8;
        }

        .footer-logo {
            margin: 10px 0;
        }

        @media (max-width: 600px) {
            .payment-options {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 2em;
            }

            .payment-card {
                padding: 20px;
            }
        }
    </style>
    <link rel="stylesheet" href="../site-helpers/site-nav.css">
</head>
<body>
    <button class="theme-switcher" onclick="cycleTheme()">🌓 Theme</button>

    <div id="nav-container"></div>

    <div class="container">
        <h1>Support tiMaxal</h1>
        
        <div class="intro">''')
        
        # Add intro text
        for text in self.config['intro_text']:
            html_parts.append(f'            <p>{text}</p>')
        
        html_parts.append('''        </div>

        <div class="payment-section">
            <h2>💳 Traditional Payment</h2>
            <div class="payment-options">''')
        
        # Add traditional payment methods
        for payment in self.config['traditional_payments']:
            safe_id = payment['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')
            html_parts.append(f'''                <div class="payment-card">
                    <h3><span class="currency-icon">{payment['icon']}</span>{payment['name']}</h3>
                    <div class="payment-info">
                        <div class="payment-label">Email:</div>
                        <div class="payment-value" id="{safe_id}-email">{payment['email']}</div>
                        <button class="copy-btn" onclick="copyToClipboard('{safe_id}-email', this)">Copy Email</button>''')
            if 'note' in payment:
                html_parts.append(f'''                        <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">{payment['note']}</p>''')
            html_parts.append('''                    </div>
                </div>''')
        
        html_parts.append('''            </div>
        </div>

        <div class="payment-section">
            <h2>₿ Cryptocurrency</h2>
            <div class="payment-options">''')
        
        # Add cryptocurrency methods
        for crypto in self.config['cryptocurrencies']:
            safe_id = crypto['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')
            html_parts.append(f'''                <div class="payment-card">
                    <h3><span class="currency-icon">{crypto['icon']}</span>{crypto['name']}</h3>
                    <div class="payment-info">''')
            
            if 'domain' in crypto:
                html_parts.append(f'''                        <div class="payment-label">Crypto Domain:</div>
                        <div class="payment-value" id="{safe_id}-domain">{crypto['domain']}</div>
                        <button class="copy-btn" onclick="copyToClipboard('{safe_id}-domain', this)">Copy Domain</button>
                        
                        <div class="payment-label" style="margin-top: 15px;">Address:</div>''')
            elif 'handle' in crypto:
                html_parts.append(f'''                        <div class="payment-label">ShakeStation Handle:</div>
                        <div class="payment-value" id="{safe_id}-handle">{crypto['handle']}</div>
                        <button class="copy-btn" onclick="copyToClipboard('{safe_id}-handle', this)">Copy Handle</button>
                        
                        <div class="payment-label" style="margin-top: 15px;">Address:</div>''')
            else:
                html_parts.append(f'''                        <div class="payment-label">Address:</div>''')
            
            html_parts.append(f'''                        <div class="payment-value" id="{safe_id}-address">{crypto['address']}</div>
                        <button class="copy-btn" onclick="copyToClipboard('{safe_id}-address', this)">Copy Address</button>
                    </div>
                </div>''')
        
        html_parts.append('''            </div>
        </div>

        <div class="back-home">
            <p><a href="../index.html">← Back to tiMaxal Hub</a></p>
        </div>

        <div id="footer-container"></div>
    </div>

    <script src="../site-helpers/theme-switcher.js"></script>
    <script src="../site-helpers/site-nav.js"></script>
    <script src="../site-helpers/footer-loader.js"></script>
    <script>
        function copyToClipboard(elementId, button) {
            const element = document.getElementById(elementId);
            const text = element.textContent;
            
            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.textContent;
                button.textContent = '✓ Copied!';
                button.classList.add('copied');
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
                button.textContent = '✗ Failed';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            });
        }
    </script>
</body>
</html>''')
        
        return '\n'.join(html_parts)
    
    def save_html(self):
        """Generate and save the HTML to the donation page."""
        html = self.generate_html()
        with open(DONATE_HTML, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ Generated {DONATE_HTML}")


def cli_mode():
    """Run in CLI mode."""
    parser = argparse.ArgumentParser(description="Manage donation page payment options")
    parser.add_argument('--add-crypto', nargs='+', metavar=('NAME', 'ICON', 'ADDRESS'),
                       help='Add cryptocurrency: NAME ICON ADDRESS [--domain DOMAIN] [--handle HANDLE]')
    parser.add_argument('--add-traditional', nargs=3, metavar=('NAME', 'ICON', 'EMAIL'),
                       help='Add traditional payment: NAME ICON EMAIL [--note NOTE]')
    parser.add_argument('--domain', help='Crypto domain for --add-crypto')
    parser.add_argument('--handle', help='Handle/username for --add-crypto')
    parser.add_argument('--note', help='Note for --add-traditional')
    parser.add_argument('--remove', metavar='NAME', help='Remove payment method by name')
    parser.add_argument('--update', metavar='NAME', help='Update payment method')
    parser.add_argument('--address', help='New address for --update')
    parser.add_argument('--email', help='New email for --update')
    parser.add_argument('--list', action='store_true', help='List all payment methods')
    parser.add_argument('--generate', action='store_true', help='Generate HTML file')
    
    args = parser.parse_args()
    manager = DonationManager()
    
    if args.list:
        manager.list_payments()
    elif args.add_crypto:
        if len(args.add_crypto) < 3:
            print("Error: --add-crypto requires NAME ICON ADDRESS")
            return
        name, icon, address = args.add_crypto[0], args.add_crypto[1], args.add_crypto[2]
        manager.add_crypto(name, icon, address, domain=args.domain, handle=args.handle)
        manager.save_html()
    elif args.add_traditional:
        name, icon, email = args.add_traditional
        manager.add_traditional(name, icon, email, note=args.note)
        manager.save_html()
    elif args.remove:
        manager.remove_payment(args.remove)
        manager.save_html()
    elif args.update:
        updates = {}
        if args.address:
            updates['address'] = args.address
        if args.email:
            updates['email'] = args.email
        if args.domain:
            updates['domain'] = args.domain
        if args.handle:
            updates['handle'] = args.handle
        if updates:
            manager.update_payment(args.update, **updates)
            manager.save_html()
        else:
            print("No updates specified")
    elif args.generate:
        manager.save_html()
    else:
        parser.print_help()


def gui_mode():
    """Launch GUI mode (requires tkinter)."""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except ImportError:
        print("Error: tkinter not available. Please use --cli flag for command-line mode.")
        return
    
    manager = DonationManager()
    
    root = tk.Tk()
    root.title("Donation Page Manager")
    root.geometry("800x600")
    
    # Create notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Tab 1: View Payments
    view_frame = ttk.Frame(notebook)
    notebook.add(view_frame, text="View Payments")
    
    text_widget = tk.Text(view_frame, wrap='word', width=80, height=30)
    text_widget.pack(fill='both', expand=True, padx=10, pady=10)
    
    def refresh_list():
        text_widget.delete('1.0', 'end')
        text_widget.insert('1.0', "=== Traditional Payments ===\n")
        for payment in manager.config["traditional_payments"]:
            text_widget.insert('end', f"\n{payment['icon']} {payment['name']}\n")
            text_widget.insert('end', f"  Email: {payment.get('email', 'N/A')}\n")
        
        text_widget.insert('end', "\n\n=== Cryptocurrencies ===\n")
        for crypto in manager.config["cryptocurrencies"]:
            text_widget.insert('end', f"\n{crypto['icon']} {crypto['name']}\n")
            if 'domain' in crypto:
                text_widget.insert('end', f"  Domain: {crypto['domain']}\n")
            if 'handle' in crypto:
                text_widget.insert('end', f"  Handle: {crypto['handle']}\n")
            text_widget.insert('end', f"  Address: {crypto['address']}\n")
    
    refresh_list()
    
    btn_frame = ttk.Frame(view_frame)
    btn_frame.pack(fill='x', padx=10, pady=5)
    
    ttk.Button(btn_frame, text="Refresh", command=refresh_list).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Generate HTML", 
               command=lambda: [manager.save_html(), messagebox.showinfo("Success", "HTML generated!")]).pack(side='left', padx=5)
    
    # Tab 2: Add Crypto
    add_crypto_frame = ttk.Frame(notebook)
    notebook.add(add_crypto_frame, text="Add Crypto")
    
    ttk.Label(add_crypto_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    crypto_name = ttk.Entry(add_crypto_frame, width=40)
    crypto_name.grid(row=0, column=1, padx=10, pady=5)
    
    ttk.Label(add_crypto_frame, text="Icon:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    crypto_icon = ttk.Entry(add_crypto_frame, width=40)
    crypto_icon.grid(row=1, column=1, padx=10, pady=5)
    
    ttk.Label(add_crypto_frame, text="Address:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    crypto_address = ttk.Entry(add_crypto_frame, width=40)
    crypto_address.grid(row=2, column=1, padx=10, pady=5)
    
    ttk.Label(add_crypto_frame, text="Domain (optional):").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    crypto_domain = ttk.Entry(add_crypto_frame, width=40)
    crypto_domain.grid(row=3, column=1, padx=10, pady=5)
    
    ttk.Label(add_crypto_frame, text="Handle (optional):").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    crypto_handle = ttk.Entry(add_crypto_frame, width=40)
    crypto_handle.grid(row=4, column=1, padx=10, pady=5)
    
    def add_crypto_action():
        name = crypto_name.get()
        icon = crypto_icon.get()
        address = crypto_address.get()
        domain = crypto_domain.get() or None
        handle = crypto_handle.get() or None
        
        if not (name and icon and address):
            messagebox.showerror("Error", "Name, Icon, and Address are required")
            return
        
        manager.add_crypto(name, icon, address, domain=domain, handle=handle)
        manager.save_html()
        messagebox.showinfo("Success", f"Added {name} and regenerated HTML")
        
        crypto_name.delete(0, 'end')
        crypto_icon.delete(0, 'end')
        crypto_address.delete(0, 'end')
        crypto_domain.delete(0, 'end')
        crypto_handle.delete(0, 'end')
        refresh_list()
    
    ttk.Button(add_crypto_frame, text="Add Cryptocurrency", command=add_crypto_action).grid(row=5, column=0, columnspan=2, pady=20)
    
    # Tab 3: Remove
    remove_frame = ttk.Frame(notebook)
    notebook.add(remove_frame, text="Remove Payment")
    
    ttk.Label(remove_frame, text="Payment Name:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    remove_name = ttk.Entry(remove_frame, width=40)
    remove_name.grid(row=0, column=1, padx=10, pady=5)
    
    def remove_action():
        name = remove_name.get()
        if not name:
            messagebox.showerror("Error", "Payment name is required")
            return
        
        if manager.remove_payment(name):
            manager.save_html()
            messagebox.showinfo("Success", f"Removed {name} and regenerated HTML")
            remove_name.delete(0, 'end')
            refresh_list()
        else:
            messagebox.showerror("Error", f"Payment method '{name}' not found")
    
    ttk.Button(remove_frame, text="Remove Payment", command=remove_action).grid(row=1, column=0, columnspan=2, pady=20)
    
    root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv or len(sys.argv) > 1:
        sys.argv.remove("--cli") if "--cli" in sys.argv else None
        cli_mode()
    else:
        gui_mode()
