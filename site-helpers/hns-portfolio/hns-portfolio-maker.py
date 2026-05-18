#!/usr/bin/env python3
"""
HNS Portfolio Maker for timax.al
Generates HTML portfolio pages from Namebase, HSD Sales Truth, Bob Wallet, and Firewallet CSV exports
Styled to match timax.al theme with 3-way theme switcher
"""

import pandas as pd
import os
import sys
import math
import json
import argparse
from pathlib import Path
from datetime import datetime
import codecs
import re
import unicodedata
import glob

# Translation library (install: pip install deep-translator)
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("Info: deep-translator not installed. Translation features will be disabled.")
    print("Install with: pip install deep-translator")

def find_csv_files(path, recursive=True):
    """Find CSV files in a directory or return single file"""
    csv_files = []
    
    if os.path.isfile(path):
        if path.lower().endswith('.csv'):
            csv_files.append(path)
    elif os.path.isdir(path):
        if recursive:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.csv'):
                        csv_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if os.path.isfile(filepath) and file.lower().endswith('.csv'):
                    csv_files.append(filepath)
    
    return sorted(csv_files)

def detect_csv_source(filepath):
    """Detect CSV source type from headers"""
    try:
        df = pd.read_csv(filepath, nrows=1)
        headers = df.columns.tolist()
        headers_lower = [h.lower() for h in headers]
        
        # Namebase Transactions: extra.domain (dot notation) is UNIQUE
        if 'extra.domain' in headers:
            return 'nb-tr'
        # HSD Sales Truth: wallet_id and ownership_status columns are UNIQUE
        elif 'wallet_id' in headers_lower and 'ownership_status' in headers_lower:
            return 'hsd'
        # Firewallet: expiry column is UNIQUE (date format, only FW has this)
        elif 'expiry' in headers_lower:
            return 'fw'
        # Namebase TLD: price_hns is UNIQUE to Namebase
        elif 'price_hns' in headers_lower:
            return 'nb-tld'
        # Bob Wallet TLD (processed): domains column (plural) with unicode/tags
        elif 'domains' in headers_lower and 'unicode' in headers_lower:
            return 'bob-tld'
        # Bob Wallet TLD (unprocessed): single column, no header or domain names
        elif len(headers) == 1:
            first_val = str(headers[0]).lower()
            # Exclude if first value is a known column name from other formats
            if first_val in ['name', 'domain', 'time', 'action', 'coin', 'expiry', 'value', 'maxbid', 'price_hns', 'for_sale']:
                return 'unknown'
            # Accept if looks like domain: xn-- prefix OR alphanumeric/hyphen/underscore <= 63 chars
            if first_val.startswith('xn--') or (len(first_val) <= 63 and all(c.isalnum() or c in '-_' for c in first_val)):
                return 'bob-tld'
        return 'unknown'
    except Exception as e:
        print(f"Error detecting source: {e}")
        return 'unknown'

def process_csv(filepath, auto_email='', include_all=False):
    """Process CSV and return list of domain dictionaries"""
    source_type = detect_csv_source(filepath)
    domains = []
    
    try:
        # Handle different CSV reading methods for malformed files
        try:
            df = pd.read_csv(filepath)
        except pd.errors.ParserError:
            try:
                df = pd.read_csv(filepath, quoting=1, escapechar='\\')
            except:
                df = pd.read_csv(filepath, on_bad_lines='skip')
        
        # For Bob TLD without header, add header
        if source_type == 'bob-tld' and len(df.columns) == 1 and 'domains' not in df.columns:
            df.columns = ['domains']
        
        # Determine domain column name
        domain_col = None
        if 'name' in df.columns:
            domain_col = 'name'
        elif 'domain' in df.columns:
            domain_col = 'domain'
        elif 'domains' in df.columns:
            domain_col = 'domains'
        elif 'extra.domain' in df.columns:
            domain_col = 'extra.domain'
        else:
            print(f"Warning: No domain column found in {os.path.basename(filepath)}")
            return domains
        
        # Determine source for marketplace linking
        if source_type.startswith('nb'):
            link_source = 'nb'
        elif source_type == 'fw':
            link_source = 'fw'
        elif source_type == 'hsd':
            link_source = 'hsd'
        elif source_type.startswith('bob'):
            link_source = 'bob'
        else:
            link_source = 'nb'  # default
        
        for _, row in df.iterrows():
            domain_name = row[domain_col]
            
            # Skip NaN domains
            if isinstance(domain_name, float) and math.isnan(domain_name):
                continue
            domain_name = str(domain_name)

            # HSD Sales Truth rows marked not for sale must never appear on the sales page.
            if source_type == 'hsd' and 'for_sale' in row.index:
                for_sale_value = row['for_sale']
                if pd.notna(for_sale_value):
                    for_sale_text = str(for_sale_value).strip().lower()
                    if for_sale_text in ['false', '0', 'no', 'n', 'off']:
                        continue
            
            # Get email and price
            email = row.get('email', row.get('eml', ''))
            # For Namebase TLD, use price_hns; otherwise try price
            if source_type == 'nb-tld':
                price = row.get('price_hns', row.get('price', ''))
            else:
                price = row.get('price', '')
            
            # Clean up nan values
            if isinstance(email, float) and math.isnan(email):
                email = ''
            if isinstance(price, float):
                if math.isnan(price):
                    price = ''
                elif price == 0.0:
                    price = ''
                else:
                    price = str(price)
            else:
                price = str(price).strip() if price else ''
                if price.lower() in ['nan', 'none', '0', '0.0']:
                    price = ''
            
            # Clean up email string
            email = str(email).strip() if email else ''
            if email.lower() in ['nan', 'none', '0']:
                email = ''
            
            # Auto-append email for domains with price if auto_email provided
            if auto_email and not email and price:
                if '@' in auto_email:
                    # If auto_email has '+' anywhere, append domain; otherwise use plain email
                    if '+' in auto_email:
                        parts = auto_email.split('@')
                        if len(parts) == 2:
                            user_part = parts[0]
                            if user_part.endswith('+'):
                                email = f"{user_part}{domain_name}@{parts[1]}"
                            else:
                                email = f"{user_part}+{domain_name}@{parts[1]}"
                    else:
                        # No '+' in email, use it as-is (plain email)
                        email = auto_email
            
            # For Bob/FW/HSD: skip domains without price (unless include_all=True)
            if link_source in ['bob', 'fw', 'hsd']:
                if not include_all and not price:
                    continue
            
            # Get descript-IDNA and description separately
            descript_idna = ''
            if 'descript-IDNA' in row.index:
                val = row['descript-IDNA']
                if pd.notna(val) and str(val).strip():
                    descript_idna = str(val)
            
            description = ''
            if 'description' in row.index:
                val = row['description']
                if pd.notna(val) and str(val).strip():
                    description = str(val)
            elif 'Description' in row.index:
                val = row['Description']
                if pd.notna(val) and str(val).strip():
                    description = str(val)
            
            translate_idna = ''
            if 'translate-IDNA' in row.index:
                val = row['translate-IDNA']
                if pd.notna(val) and str(val).strip():
                    translate_idna = str(val)
            
            domain = {
                'name': domain_name,
                'unicode': row.get('unicode', ''),
                'descript': descript_idna,
                'description': description,
                'translate': translate_idna,
                'tags': row.get('tags', 'All Names'),
                'source': link_source,
                'email': email,
                'price': price
            }
            domains.append(domain)
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return domains

def format_domain_link(domain, include_descriptions=False):
    """Format domain as HTML link with appropriate marketplace or contact info"""
    name = domain['name']
    unicode_val = str(domain.get('unicode', ''))
    source = domain.get('source', 'nb')
    email = domain.get('email', '')
    price = domain.get('price', '')
    tags = domain.get('tags', '')
    descript = str(domain.get('descript', ''))  # descript-IDNA (italic)
    description = str(domain.get('description', ''))  # description (quotes)
    translate = str(domain.get('translate', ''))  # translate-IDNA (quotes)
    
    # Clean up nan values
    if descript.lower() == 'nan' or not descript:
        descript = ''
    if description.lower() == 'nan' or not description:
        description = ''
    if translate.lower() == 'nan' or not translate:
        translate = ''
    
    # Format display name
    if name.startswith('xn--'):
        if unicode_val and unicode_val.lower() != 'nan' and unicode_val.strip():
            try:
                unicode_bytes = codecs.decode(unicode_val, 'unicode_escape')
                unicode_char = unicode_bytes.encode('latin-1').decode('utf-8')
            except:
                unicode_char = unicode_val
            display_name = f'{unicode_char} <span class="puny">({name})</span>'
        else:
            display_name = name
    else:
        display_name = name
    
    # Determine marketplace URL or contact display
    if source == 'nb':
        base_url = f"https://www.namebase.io/domains/{name}"
        link_html = f'<a href="{base_url}" target="_blank" rel="noreferrer">{display_name}</a>'
    elif source in ['bob', 'fw', 'hsd']:
        # Bob/Firewallet/HSD: No marketplace link, show contact info
        link_html = f'<span class="domain-name-only">{display_name}</span>'
    else:
        # Default to Namebase
        base_url = f"https://www.namebase.io/domains/{name}"
        link_html = f'<a href="{base_url}" target="_blank" rel="noreferrer">{display_name}</a>'
    
    # Build HTML parts
    html_parts = [link_html]
    
    # Add descriptions if enabled
    if include_descriptions:
        desc_parts = []
        # descript-IDNA: italics, no quotes
        if descript:
            desc_parts.append(f'<span class="desc-text"><i>{descript}</i></span>')
        # description: quotes, no italics
        if description:
            desc_parts.append(f'<span class="description-text">"{description}"</span>')
        # translate-IDNA: quotes, no italics
        if translate:
            desc_parts.append(f'<span class="translate-text">"{translate}"</span>')
        if desc_parts:
            html_parts.append(f'<div class="domain-descriptions">{" ".join(desc_parts)}</div>')
    
    # Add contact info
    contact_parts = []
    # Only add @eml button for Bob/FW/HSD (non-marketplace) domains with email template ('+' present)
    if source in ['bob', 'fw', 'hsd'] and email and '+' in email:
        copy_btn = f'<button class="copy-email-btn" onclick="copyEmail(event, \'{email}\')" title="Copy {email}">@eml</button>'
        contact_parts.append(copy_btn)
    # Price goes to the right of email button
    if price:
        # Show as HNS, keep decimals only if present
        try:
            price_float = float(price)
            if price_float == int(price_float):
                contact_parts.append(f'<span class="price-tag">{int(price_float)} HNS</span>')
            else:
                contact_parts.append(f'<span class="price-tag">{price} HNS</span>')
        except:
            contact_parts.append(f'<span class="price-tag">{price} HNS</span>')
    
    if contact_parts:
        html_parts.append(f'<div class="domain-contact">{" ".join(contact_parts)}</div>')
    
    return f'<div class="domain-with-contact" data-price="{price if price else ""}" data-email="{email if email else ""}" data-tags="{tags}" data-puny="{"true" if name.startswith("xn--") else "false"}">{"".join(html_parts)}</div>'


def show_help():
    """Display comprehensive help information"""
    help_text = """
HNS PORTFOLIO MAKER - HELP
========================================================================================

DESCRIPTION:
    CLI tool for generating HNS portfolio HTML pages with timax.al site integration.
    Supports Namebase, HSD Sales Truth, Bob Wallet, and Firewallet CSV exports.

USAGE:
    python hns-portfolio-maker.py [csv_files_or_directories...]
    python hns-portfolio-maker.py                    # Interactive menu mode

EXAMPLES:
    # Process single CSV file
    python hns-portfolio-maker.py domains.csv
    
    # Process multiple files
    python hns-portfolio-maker.py file1.csv file2.csv file3.csv
    
    # Process entire directory (recursive)
    python hns-portfolio-maker.py csv-s/
    
    # Use settings file
    python hns-portfolio-maker.py    # Choose option 1 from menu

SUPPORTED CSV FORMATS:
    - Namebase TLD exports (name, unicode, tags, price, email)
    - Namebase Transactions (extra.domain)
    - HSD Sales Truth (domains, wallet_id, ownership_status)
    - Bob Wallet TLD (domains column or single-column format)
    - Firewallet exports (expiry column)

CSV REQUIREMENTS (if not using "all": true):
    - Bob/Firewallet/HSD domains require email OR price column
    - Optional columns: unicode, descript-IDNA, translate-IDNA, tags

SETTINGS FILE (portfolio-settings.json):
    Create a settings file in the script directory with:
    {
      "csv_files": ["path/to/file1.csv", "csv-s"],
      "output_filename": "my-portfolio.html",
      "title": "My HNS Portfolio",
      "email": "user+@gmail.com",
      "credits_file": "html/credits.html",
      "include_descriptions": true,
      "all": false
    }
    
FEATURES:
    Auto-detects CSV format (nb, bob, fw, hsd)
    Marketplace linking (Namebase)
    Contact info display (price, email with copy button)
    Auto-email append for domains with price
    Search & filter (text, price range, tags)
    5 sort modes (Random, A-Z, Z-A, Price up, Price down)
    Grid/List view toggle
    Description/translation display toggle
    3-way theme switcher (Light/Dark/Black)
    Full timax.al site integration
    Recursive directory search (specify directories in csv_files)
    Domain filtering: "all": true/false (default false)
      - false: only domains with price (Bob/FW)
      - true: ALL domains regardless of price
    Requirements check (auto-detects and offers to install packages)

OUTPUT LOCATION:
    ../../HTML/sellhns/ (relative to script)

MORE INFO:
    See hns-portfolio-maker.README.md for complete documentation.

========================================================================================
"""
    print(help_text)


def expand_csv_paths(paths_or_dirs):
    """Expand paths - if directory, recursively find all CSV files"""
    csv_files = []
    
    for path in paths_or_dirs:
        path_obj = Path(path)
        
        if path_obj.is_file() and str(path).endswith('.csv'):
            # Direct CSV file
            csv_files.append(str(path_obj))
        elif path_obj.is_dir():
            # Directory - find all CSV files recursively
            pattern = str(path_obj / '**' / '*.csv')
            found_files = glob.glob(pattern, recursive=True)
            csv_files.extend(found_files)
            print(f"  Found {len(found_files)} CSV files in {path}")
        else:
            print(f"  [WARNING]: Skipping invalid path: {path}")
    
    return csv_files

def load_settings_if_exists():
    """Auto-load portfolio-settings.json if it exists in script directory"""
    script_dir = Path(__file__).parent
    settings_file = script_dir / "portfolio-settings.json"
    
    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            print(f"\n[OK] Loaded settings from: {settings_file.name}")
            
            # Expand CSV paths (files or directories)
            if 'csv_files' in settings:
                print(f"\n[INFO] Expanding CSV paths...")
                expanded_files = expand_csv_paths(settings['csv_files'])
                settings['csv_files'] = expanded_files
                print(f"  Total CSV files to process: {len(expanded_files)}")
            
            return settings
        except Exception as e:
            print(f"\n[WARNING]: Could not load {settings_file.name}: {e}")
            return None
    return None

def generate_html(domains, output_filename="portfolio.html", title="HNS Portfolio", credits_file=None, include_descriptions=False, has_email=False, plain_email=''):
    """Generate HTML with timax.al theming"""

    # Create info banner based on email type
    info_banner = ''
    if plain_email:
        # Plain email without '+' - show email in banner, no copy buttons
        info_banner = f'''
        <div class="info-banner">
            <p>Namebase domains have marketplace links. For other domains, email <a href="mailto:{plain_email}">{plain_email}</a> with queries or offers.</p>
        </div>
        '''
    elif has_email:
        # Email with '+' - show copy buttons, explain non-custodial domains
        info_banner = '''
        <div class="info-banner">
            <p>Namebase domains have marketplace links. Non-custodial domains show email for queries or offers.</p>
        </div>
        '''
    
    # Conditional desc button based on include_descriptions setting
    desc_button_html = '<button id="descToggleBtn" class="desc-toggle-button" onclick="toggleDescriptions()">Show Descripts</button>' if include_descriptions else ''

    # Organize domains by tags
    tags_dict = {}
    for domain in domains:
        tags_list = str(domain['tags']).split(',')
        for tag in tags_list:
            tag = tag.strip()
            if not tag:
                tag = 'All Names'
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append(domain)
    
    # Ensure 'All Names' exists (add all domains if no empty tags found)
    if 'All Names' not in tags_dict:
        tags_dict['All Names'] = list(domains)

    # Sort tags: 'All Names' first, then alphabetical (filter out nan/empty)
    valid_tags = [tag for tag in tags_dict.keys() if tag and str(tag).lower() not in ['nan', '']]
    tags_sorted = ['All Names'] + sorted(set(valid_tags) - {'All Names'})
    
    # Generate sections
    sections = []
    for tag in tags_sorted:
        section_id = tag.lower().replace(' ', '-')
        domain_links = [f'<div class="domain-item">{format_domain_link(d, include_descriptions)}</div>'
                       for d in tags_dict[tag]]
        sections.append(f'''
        <div id="{section_id}" class="tag-section">
            <h3>{tag}</h3>
            <div class="domain-grid">
                {''.join(domain_links)}
            </div>
        </div>
        ''')
    
    # Load credits content if provided (moved outside loop!)
    credits_html = ''
    if credits_file and os.path.exists(credits_file):
        with open(credits_file, 'r', encoding='utf-8') as f:
            credits_content = f.read()
            credits_html = f'''
        <div class="credits-section">
            {credits_content}
        </div>
        '''
    
    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        /* Light theme (default) */
        body {{
            background-color: #ccffff;
            color: #3404f4;
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.6;
            padding: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        /* Dark theme */
        body.dark-theme {{
            background-color: #003366;
            color: #99ddff;
        }}
        
        /* Black theme */
        body.black-theme {{
            background-color: #000000;
            color: #ffffff;
        }}
        
        a:link {{ color: #0000ee; text-decoration: none; }}
        a:visited {{ color: #551a8b; }}
        a:hover {{ color: #3404f4; text-decoration: underline; }}
        
        body.dark-theme a:link {{ color: #66bbff; }}
        body.dark-theme a:visited {{ color: #9988ff; }}
        body.dark-theme a:hover {{ color: #99ddff; }}
        
        body.black-theme a:link {{ color: #66bbff; }}
        body.black-theme a:visited {{ color: #9999ff; }}
        body.black-theme a:hover {{ color: #ffffff; }}
        
        /* Button container - fixed position for all control buttons */
        .buttons-container {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            align-items: flex-end;
        }}
        
        .buttons-container button {{
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
            min-width: 120px;
        }}
        
        .buttons-container button:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        }}
        
        body.dark-theme .buttons-container button {{
            background-color: rgba(153, 221, 255, 0.8);
            color: #003366;
        }}
        
        body.black-theme .buttons-container button {{
            background-color: rgba(255, 255, 255, 0.8);
            color: #000000;
        }}
        
        /* Legacy button styles for compatibility */
        .theme-switcher {{
            /* Styles now handled by buttons-container */
        }}
        
        .theme-switcher:hover {{
            /* Handled by buttons-container */
        }}
        
        body.dark-theme .theme-switcher {{
            /* Handled by buttons-container */
        }}
        
        body.black-theme .theme-switcher {{
            /* Handled by buttons-container */
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid currentColor;
        }}
        
        .search-box {{
            text-align: center;
            margin: 20px 0;
        }}
        
        .search-box input {{
            width: 100%;
            max-width: 500px;
            padding: 10px 15px;
            font-size: 1em;
            border: 2px solid currentColor;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.1);
            color: inherit;
        }}
        
        .tag-section {{
            display: block;
            margin: 0;
            padding: 0;
        }}
        
        .tag-section.hidden {{
            display: none !important;
        }}
        
        .tag-section.active {{
            display: block;
        }}
        
        .tag-section#all-names {{
            display: block;
        }}
        
        .tag-section h3 {{
            display: none;
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .domain-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            padding: 10px;
        }}
        
        .domain-item {{
            padding: 12px;
            background-color: rgba(52, 4, 244, 0.05);
            border: 1px solid currentColor;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .domain-item:hover {{
            background-color: rgba(52, 4, 244, 0.15);
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        body.dark-theme .domain-item {{
            background-color: rgba(153, 221, 255, 0.05);
        }}
        
        body.dark-theme .domain-item:hover {{
            background-color: rgba(153, 221, 255, 0.15);
        }}
        
        body.black-theme .domain-item {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        
        body.black-theme .domain-item:hover {{
            background-color: rgba(255, 255, 255, 0.15);
        }}
        
        .puny {{
            font-size: 0.8em;
            opacity: 0.7;
        }}

        /* Info banner */
        .info-banner {{
            padding: 1em;
            margin: 10px 0;
            background-color: rgba(52, 4, 244, 0.1);
            border-radius: 5px;
            text-align: center;
        }}

        body.dark-theme .info-banner {{
            background-color: rgba(153, 221, 255, 0.1);
        }}

        body.black-theme .info-banner {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        /* Marketplace links section */
        .marketplace-section {{
            padding: 1em;
            background-color: rgba(52, 4, 244, 0.08);
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        body.dark-theme .marketplace-section {{
            background-color: rgba(153, 221, 255, 0.08);
        }}
        
        body.black-theme .marketplace-section {{
            background-color: rgba(255, 255, 255, 0.08);
        }}
        
        .marketplace-label {{
            font-weight: bold;
            text-align: center;
            margin-bottom: 1em;
            font-size: 1.1em;
        }}
        
        .marketplace-links {{
            display: flex;
            justify-content: center;
            gap: 1em;
            flex-wrap: wrap;
        }}
        
        .marketplace-links a {{
            padding: 0.5em 1em;
            background-color: rgba(52, 4, 244, 0.2);
            color: inherit;
            border: 2px solid currentColor;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s ease;
            text-align: center;
            flex: 0 1 auto;
        }}
        
        .marketplace-links a:hover {{
            background-color: rgba(52, 4, 244, 0.4);
            transform: scale(1.05);
        }}
        
        body.dark-theme .marketplace-links a {{
            background-color: rgba(153, 221, 255, 0.2);
        }}
        
        body.dark-theme .marketplace-links a:hover {{
            background-color: rgba(153, 221, 255, 0.4);
        }}
        
        body.black-theme .marketplace-links a {{
            background-color: rgba(255, 255, 255, 0.2);
        }}
        
        body.black-theme .marketplace-links a:hover {{
            background-color: rgba(255, 255, 255, 0.4);
        }}
        
        /* Contact info and price styles */
        .domain-with-contact {{
            display: flex;
            flex-direction: column;
            gap: 0.3em;
        }}
        
        .domain-name-only {{
            font-weight: bold;
        }}
        
        .domain-contact {{
            font-size: 0.9em;
            display: flex;
            gap: 0.5em;
            justify-content: center;
            align-items: center;
        }}
        
        .price-tag {{
            padding: 0.2em 0.5em;
            background-color: rgba(52, 4, 244, 0.15);
            border-radius: 4px;
            font-weight: bold;
        }}
        
        body.dark-theme .price-tag {{
            background-color: rgba(153, 221, 255, 0.15);
        }}
        
        body.black-theme .price-tag {{
            background-color: rgba(255, 255, 255, 0.15);
        }}
        
        .copy-email-btn {{
            padding: 0.2em 0.5em;
            background-color: rgba(52, 4, 244, 0.15);
            border: 1px solid currentColor;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s ease;
        }}
        
        .copy-email-btn:hover {{
            background-color: rgba(52, 4, 244, 0.3);
            transform: scale(1.1);
        }}
        
        body.dark-theme .copy-email-btn {{
            background-color: rgba(153, 221, 255, 0.15);
        }}
        
        body.dark-theme .copy-email-btn:hover {{
            background-color: rgba(153, 221, 255, 0.3);
        }}
        
        body.black-theme .copy-email-btn {{
            background-color: rgba(255, 255, 255, 0.15);
        }}
        
        body.black-theme .copy-email-btn:hover {{
            background-color: rgba(255, 255, 255, 0.3);
        }}
        
        /* Description and translation styles */
        .domain-descriptions {{
            font-size: 0.85em;
            margin-top: 0.3em;
            display: flex;
            flex-direction: column;
            gap: 0.2em;
        }}
        
        body.hide-descriptions .domain-descriptions {{
            display: none;
        }}
        
        .desc-text {{
            color: inherit;
            opacity: 0.9;
        }}
        
        .translate-text {{
            color: inherit;
            opacity: 0.85;
            font-style: italic;
        }}
        
        /* Filter controls */
        .filter-controls {{
            display: flex;
            gap: 0.5em;
            padding: 1em;
            justify-content: center;
            flex-wrap: wrap;
            background-color: rgba(52, 4, 244, 0.08);
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        body.dark-theme .filter-controls {{
            background-color: rgba(153, 221, 255, 0.08);
        }}
        
        body.black-theme .filter-controls {{
            background-color: rgba(255, 255, 255, 0.08);
        }}
        
        .filter-controls input,
        .filter-controls select,
        .filter-controls button {{
            padding: 0.5em;
            border: 2px solid currentColor;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.1);
            color: inherit;
            font-family: inherit;
        }}
        
        .filter-controls button {{
            background-color: rgba(52, 4, 244, 0.2);
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .filter-controls button:hover {{
            background-color: rgba(52, 4, 244, 0.4);
        }}
        
        body.dark-theme .filter-controls button {{
            background-color: rgba(153, 221, 255, 0.2);
        }}
        
        body.dark-theme .filter-controls button:hover {{
            background-color: rgba(153, 221, 255, 0.4);
        }}
        
        body.black-theme .filter-controls button {{
            background-color: rgba(255, 255, 255, 0.2);
        }}
        
        body.black-theme .filter-controls button:hover {{
            background-color: rgba(255, 255, 255, 0.4);
        }}
        
        /* Individual button styles now handled by buttons-container */
        
        /* List view styles */
        .domain-grid.list-view {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .domain-grid.list-view .domain-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-align: left;
        }}
        
        .domain-grid.list-view .domain-with-contact {{
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 1em;
            width: 100%;
        }}
        
        .domain-grid.list-view .domain-descriptions {{
            margin-left: auto;
            text-align: right;
            flex-shrink: 0;
        }}
        
        .domain-grid.list-view .domain-contact {{
            margin-left: auto;
            flex-shrink: 0;
        }}
        
        /* Credits section */
        .credits-section {{
            margin-top: 2em;
            padding: 1.5em;
            border-top: 2px solid currentColor;
            background-color: rgba(52, 4, 244, 0.08);
            border-radius: 8px;
            color: inherit;
        }}
        
        body.dark-theme .credits-section {{
            background-color: rgba(153, 221, 255, 0.08);
        }}
        
        body.black-theme .credits-section {{
            background-color: rgba(255, 255, 255, 0.08);
        }}
        
        .credits-section * {{
            color: inherit !important;
        }}
        
        /* Pagination controls */
        .pagination-controls {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1em;
            margin: 2em 0;
            padding: 1em;
            background-color: rgba(52, 4, 244, 0.08);
            border-radius: 10px;
            flex-wrap: wrap;
        }}
        
        body.dark-theme .pagination-controls {{
            background-color: rgba(153, 221, 255, 0.08);
        }}
        
        body.black-theme .pagination-controls {{
            background-color: rgba(255, 255, 255, 0.08);
        }}
        
        .pagination-controls button {{
            padding: 0.5em 1em;
            background-color: rgba(52, 4, 244, 0.2);
            color: inherit;
            border: 2px solid currentColor;
            border-radius: 8px;
            cursor: pointer;
            font-family: inherit;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        
        .pagination-controls button:hover:not(:disabled) {{
            background-color: rgba(52, 4, 244, 0.4);
            transform: scale(1.05);
        }}
        
        .pagination-controls button:disabled {{
            opacity: 0.4;
            cursor: not-allowed;
        }}
        
        body.dark-theme .pagination-controls button {{
            background-color: rgba(153, 221, 255, 0.2);
        }}
        
        body.dark-theme .pagination-controls button:hover:not(:disabled) {{
            background-color: rgba(153, 221, 255, 0.4);
        }}
        
        body.black-theme .pagination-controls button {{
            background-color: rgba(255, 255, 255, 0.2);
        }}
        
        body.black-theme .pagination-controls button:hover:not(:disabled) {{
            background-color: rgba(255, 255, 255, 0.4);
        }}
        
        .pagination-info {{
            font-weight: bold;
            padding: 0 1em;
        }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 30px;
            text-align: center;
            border-top: 2px solid currentColor;
        }}
    </style>
    <link rel="stylesheet" href="../../helpers/site-nav.css?v=2">
    <script src="../../helpers/theme-switcher.js?v=2"></script>
    <script src="../../helpers/footer-loader.js?v=2"></script>
    <script src="../../helpers/site-nav.js?v=2"></script>
</head>
<body>
    <div class="buttons-container">
        <button id="themeBtn" class="theme-switcher" onclick="cycleTheme()">☀️ Light</button>
        <button id="sortBtn" class="sort-button" onclick="cycleSortTLDs()">Sort: Random</button>
        <button id="viewToggleBtn" class="view-toggle-button" onclick="toggleView()">📊 Grid</button>
        {desc_button_html}
    </div>
    
    <div id="nav-container"></div>
    
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>

        <!-- Marketplace Links -->
        <div class="marketplace-section">
            <div class="marketplace-label">Access Handshake:</div>
            <div class="marketplace-links">
                <a href="https://handshake.org/" target="_blank" rel="noreferrer">Handshake</a>
                <a href="https://shakeshift.com/names" target="_blank" rel="noreferrer">ShakeShift</a>
                <a href="https://bobwallet.io" target="_blank" rel="noreferrer">Bob Wallet</a>
                <a href="https://www.namebase.io" target="_blank" rel="noreferrer">Namebase</a>
                <a href="https://impervious.com/fingertip" target="_blank" rel="noreferrer">Fingertip</a>
                <a href="https://git.woodburn.au/nathanwoodburn/firewalletbrowser" target="_blank" rel="noreferrer">FireWallet</a>
            </div>
        </div>
        
        <!-- Filter Controls -->
        <div class="filter-controls">
            <input type="text" id="searchInput" placeholder="Search domains..." onkeyup="filterDomains()">
            <input type="number" id="minPrice" placeholder="Min price (HNS)" step="0.01" onchange="filterDomains()">
            <input type="number" id="maxPrice" placeholder="Max price (HNS)" step="0.01" onchange="filterDomains()">
            <select id="tagFilter" onchange="filterDomains()">
                <option value="">All Tags</option>
            </select>
            <button id="buyNowBtn" onclick="toggleBuyNowFilter()">'Buy now' Only</button>
            <select id="perPageSelect" onchange="updatePerPage()">
                <option value="50">50 per page</option>
                <option value="100" selected>100 per page</option>
                <option value="500">500 per page</option>
                <option value="all">All</option>
            </select>
            <button onclick="clearFilters()">Clear Filters</button>
        </div>
        
        <!-- Pagination Controls -->
        <div id="paginationControls" class="pagination-controls" style="display: none;">
            <button id="prevPageBtn" onclick="goToPage(currentPage - 1)">← Previous</button>
            <span class="pagination-info" id="paginationInfo">Page 1 of 1</span>
            <span id="goToPageContainer" style="display: none;">
                Go to: <input type="number" id="goToPageInput" min="1" style="width: 60px; padding: 0.3em; border: 2px solid currentColor; border-radius: 5px; background: rgba(255,255,255,0.1); color: inherit;" onkeypress="if(event.key==='Enter') goToPageFromInput()">
                <button onclick="goToPageFromInput()" style="padding: 0.3em 0.8em;">Go</button>
            </span>
            <button id="nextPageBtn" onclick="goToPage(currentPage + 1)">Next →</button>
        </div>

        <!-- Info Banner (when email is provided) -->
        {info_banner}
        
        {''.join(sections)}
        
        {credits_html}
        
        <div id="footer-container"></div>
    </div>
    
    <script>
        let sortState = 0; // 0=random, 1=a-z, 2=z-a, 3=price-low, 4=price-high
        let buyNowFilterActive = false; // Track buy now filter state
        let perPageLimit = '100'; // Track per-page limit
        let currentPage = 1; // Track current page
        let totalPages = 1; // Track total pages
        
        // Site's theme-switcher.js handles all theme functionality
        // No custom theme code needed
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Site's theme-switcher.js handles theme button initialization
            
            showSection('all-names');
            populateTagFilter();
            randomizeMarketplaceLinks();
            
            // Initialize per-page limit
            perPageLimit = document.getElementById('perPageSelect').value;
            applyPagination();
        }});

        function showSection(sectionId) {{
            // Hide all sections
            const sections = document.querySelectorAll('.tag-section');
            sections.forEach(s => s.classList.remove('active'));
            
            // Show selected section
            const section = document.getElementById(sectionId);
            if (section) {{
                section.classList.add('active');
            }}
        }}
        
        function cycleSortTLDs() {{
            const sortBtn = document.getElementById('sortBtn');
            const currentSection = document.querySelector('.tag-section.active');
            if (!currentSection) return;
            
            const grid = currentSection.querySelector('.domain-grid');
            const items = Array.from(grid.querySelectorAll('.domain-item'));
            
            sortState = (sortState + 1) % 5;
            
            // Don't reset visibility - preserve current filter state
            
            switch(sortState) {{
                case 0: // Random
                    for (let i = items.length - 1; i > 0; i--) {{
                        const j = Math.floor(Math.random() * (i + 1));
                        [items[i], items[j]] = [items[j], items[i]];
                    }}
                    sortBtn.textContent = 'Sort: Random';
                    break;
                case 1: // A-Z
                    items.sort((a, b) => a.textContent.toLowerCase().localeCompare(b.textContent.toLowerCase()));
                    sortBtn.textContent = 'Sort: A-Z ^';
                    break;
                case 2: // Z-A
                    items.sort((a, b) => b.textContent.toLowerCase().localeCompare(a.textContent.toLowerCase()));
                    sortBtn.textContent = 'Sort: Z-A v';
                    break;
                case 3: // Price Low-High
                    items.sort((a, b) => {{
                        const priceA = parseFloat(a.querySelector('.domain-with-contact')?.dataset?.price || '999999');
                        const priceB = parseFloat(b.querySelector('.domain-with-contact')?.dataset?.price || '999999');
                        return priceA - priceB;
                    }});
                    sortBtn.textContent = 'Sort: Price ^';
                    break;
                case 4: // Price High-Low
                    items.sort((a, b) => {{
                        const priceA = parseFloat(a.querySelector('.domain-with-contact')?.dataset?.price || '0');
                        const priceB = parseFloat(b.querySelector('.domain-with-contact')?.dataset?.price || '0');
                        return priceB - priceA;
                    }});
                    sortBtn.textContent = 'Sort: Price v';
                    break;
            }}
            
            grid.innerHTML = '';
            items.forEach(item => grid.appendChild(item));
        }}
        
        function toggleView() {{
            const viewToggleBtn = document.getElementById('viewToggleBtn');
            const grids = document.querySelectorAll('.domain-grid');
            
            grids.forEach(grid => {{
                grid.classList.toggle('list-view');
            }});
            
            // Update button text - INVERTED: show Grid when in list view, List when in grid view
            if (document.querySelector('.domain-grid.list-view')) {{
                viewToggleBtn.textContent = '📊 Grid';
            }} else {{
                viewToggleBtn.textContent = '📋 List';
            }}
        }}
        
        function toggleDescriptions() {{
            const descToggleBtn = document.getElementById('descToggleBtn');
            document.body.classList.toggle('hide-descriptions');
            
            // Update button text
            if (document.body.classList.contains('hide-descriptions')) {{
                descToggleBtn.textContent = 'Show Descripts';
            }} else {{
                descToggleBtn.textContent = 'Hide Descripts';
            }}
        }}
        
        function populateTagFilter() {{
            const tagFilter = document.getElementById('tagFilter');
            const allTags = new Set();
            
            document.querySelectorAll('.domain-with-contact').forEach(item => {{
                const tags = item.dataset.tags?.split(',') || [];
                tags.forEach(tag => {{
                    const trimmedTag = tag.trim();
                    // Filter out empty, 'All Names', and 'nan' tags
                    if (trimmedTag && trimmedTag !== 'All Names' && trimmedTag.toLowerCase() !== 'nan') {{
                        allTags.add(trimmedTag);
                    }}
                }});
            }});
            
            // Add 'Buy now' Only option
            const buyNowOption = document.createElement('option');
            buyNowOption.value = '__BUY_NOW__';
            buyNowOption.textContent = "'Buy now' Only";
            tagFilter.appendChild(buyNowOption);
            
            // Add special 'No PUNY' filter option
            const punyOption = document.createElement('option');
            punyOption.value = '__NO_PUNY__';
            punyOption.textContent = "No 'PUNY'";
            tagFilter.appendChild(punyOption);
            
            // Add separator
            const separator = document.createElement('option');
            separator.disabled = true;
            separator.textContent = '───────────';
            tagFilter.appendChild(separator);
            
            // Then add all regular tags sorted
            Array.from(allTags).sort().forEach(tag => {{
                const option = document.createElement('option');
                option.value = tag;
                option.textContent = tag;
                tagFilter.appendChild(option);
            }});
        }}
        
        function filterDomains() {{
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const minPrice = parseFloat(document.getElementById('minPrice').value) || null;
            const maxPrice = parseFloat(document.getElementById('maxPrice').value) || null;
            const tagFilter = document.getElementById('tagFilter').value;
            
            // Show/hide tag sections based on filter
            const sections = document.querySelectorAll('.tag-section');
            sections.forEach(section => {{
                section.classList.remove('hidden');
                
                if (tagFilter && tagFilter !== '__BUY_NOW__' && tagFilter !== '__NO_PUNY__') {{
                    // When filtering by specific tag, hide all sections except matching one
                    const sectionId = section.id;
                    const sectionTag = sectionId.replace(/-/g, ' ');
                    if (sectionId !== 'all-names' && sectionTag !== tagFilter.toLowerCase()) {{
                        section.classList.add('hidden');
                    }}
                }}
            }});
            
            const items = document.querySelectorAll('.domain-item');
            
            items.forEach(item => {{
                // Search only domain links, not email/price text
                const domainLinks = item.querySelectorAll('a, .domain-name-only');
                const domainText = Array.from(domainLinks).map(link => link.textContent.toLowerCase()).join(' ');
                const domainDiv = item.querySelector('.domain-with-contact');

                // Text search - only in domain names
                let textMatch = domainText.includes(searchInput);
                
                // Price filter
                let priceMatch = true;
                if (minPrice || maxPrice) {{
                    const priceData = domainDiv?.dataset?.price;
                    if (priceData) {{
                        const price = parseFloat(priceData);
                        if (minPrice && price < minPrice) {{
                            priceMatch = false;
                        }}
                        if (maxPrice && price > maxPrice) {{
                            priceMatch = false;
                        }}
                    }} else {{
                        priceMatch = false;
                    }}
                }}
                
                // Buy now filter (marketplace links only - nb/ss sources)
                let buyNowMatch = true;
                if (buyNowFilterActive || tagFilter === '__BUY_NOW__') {{
                    // Check if domain has marketplace link (a tag exists)
                    const hasMarketplaceLink = item.querySelector('a[href]');
                    if (!hasMarketplaceLink) {{
                        buyNowMatch = false;
                    }}
                }}
                
                // Tag filter
                let tagMatch = true;
                if (tagFilter && domainDiv) {{
                    if (tagFilter === '__NO_PUNY__') {{
                        // Special case: hide PUNY names
                        const isPuny = domainDiv?.dataset?.puny === 'true';
                        if (isPuny) {{
                            tagMatch = false;
                        }}
                    }} else if (tagFilter === '__BUY_NOW__') {{
                        // Handled by buyNowMatch above
                        tagMatch = true;
                    }} else {{
                        const tags = domainDiv.dataset.tags?.split(',').map(t => t.trim()) || [];
                        tagMatch = tags.includes(tagFilter);
                    }}
                }}
                
                if (textMatch && priceMatch && buyNowMatch && tagMatch) {{
                    item.style.display = '';
                    item.removeAttribute('data-filter-hidden');
                }} else {{
                    item.style.display = 'none';
                    item.setAttribute('data-filter-hidden', 'true');
                }}
            }});
            
            // Reset to page 1 when filters change
            currentPage = 1;
            
            // Apply pagination after filtering
            applyPagination();
        }}
        
        function toggleBuyNowFilter() {{
            buyNowFilterActive = !buyNowFilterActive;
            const buyNowBtn = document.getElementById('buyNowBtn');
            
            if (buyNowFilterActive) {{
                buyNowBtn.style.backgroundColor = 'rgba(52, 4, 244, 0.5)';
                buyNowBtn.style.fontWeight = 'bold';
            }} else {{
                buyNowBtn.style.backgroundColor = '';
                buyNowBtn.style.fontWeight = '';
            }}
            
            filterDomains();
        }}
        
        function updatePerPage() {{
            perPageLimit = document.getElementById('perPageSelect').value;
            currentPage = 1; // Reset to first page when changing limit
            applyPagination();
        }}
        
        function applyPagination() {{
            const items = document.querySelectorAll('.domain-item');
            const allItems = Array.from(items);
            
            // Get items not hidden by filters and deduplicate by domain name
            const seenDomains = new Set();
            const availableItems = [];
            
            allItems.forEach(item => {{
                if (!item.hasAttribute('data-filter-hidden')) {{
                    // Get domain name from the item for deduplication
                    const domainDiv = item.querySelector('.domain-with-contact');
                    const domainLink = item.querySelector('a, .domain-name-only');
                    const domainName = domainLink ? domainLink.textContent.trim() : '';
                    
                    // Only include if we haven't seen this domain yet
                    if (domainName && !seenDomains.has(domainName)) {{
                        seenDomains.add(domainName);
                        availableItems.push(item);
                    }} else if (!domainName) {{
                        // If we can't get domain name, include it anyway
                        availableItems.push(item);
                    }}
                }}
            }});
            
            const totalItems = availableItems.length;
            
            // Hide pagination controls if showing all or no items
            const paginationControls = document.getElementById('paginationControls');
            const goToPageContainer = document.getElementById('goToPageContainer');
            
            if (perPageLimit === 'all' || totalItems === 0) {{
                // Show all items that aren't filtered out
                availableItems.forEach(item => {{
                    item.style.display = '';
                }});
                if (paginationControls) paginationControls.style.display = 'none';
                return;
            }}
            
            const limit = parseInt(perPageLimit);
            totalPages = Math.max(1, Math.ceil(totalItems / limit));
            
            // Ensure current page is valid
            if (currentPage > totalPages) currentPage = totalPages;
            if (currentPage < 1) currentPage = 1;
            
            // Show pagination controls
            if (paginationControls) paginationControls.style.display = 'flex';
            
            // Show/hide go-to-page input based on total pages
            if (goToPageContainer) {{
                goToPageContainer.style.display = totalPages > 6 ? 'inline' : 'none';
            }}
            
            // Calculate start and end indices
            const startIdx = (currentPage - 1) * limit;
            const endIdx = Math.min(startIdx + limit, totalItems);
            
            // Hide all items first
            allItems.forEach(item => {{
                item.style.display = 'none';
            }});
            
            // Show only items in current page range from available items
            for (let i = startIdx; i < endIdx && i < availableItems.length; i++) {{
                availableItems[i].style.display = '';
            }}
            
            // Update pagination info
            updatePaginationControls(totalItems);
        }}
        
        function updatePaginationControls(totalItems) {{
            const paginationInfo = document.getElementById('paginationInfo');
            const prevBtn = document.getElementById('prevPageBtn');
            const nextBtn = document.getElementById('nextPageBtn');
            const goToPageInput = document.getElementById('goToPageInput');
            
            if (paginationInfo) {{
                paginationInfo.textContent = `Page ${{currentPage}} of ${{totalPages}} (${{totalItems}} items)`;
            }}
            
            if (prevBtn) {{
                prevBtn.disabled = currentPage <= 1;
            }}
            
            if (nextBtn) {{
                nextBtn.disabled = currentPage >= totalPages;
            }}
            
            if (goToPageInput) {{
                goToPageInput.max = totalPages;
                goToPageInput.placeholder = `1-${{totalPages}}`;
            }}
        }}
        
        function goToPage(page) {{
            if (page < 1 || page > totalPages) return;
            currentPage = page;
            applyPagination();
        }}
        
        function goToPageFromInput() {{
            const input = document.getElementById('goToPageInput');
            if (!input) return;
            
            const page = parseInt(input.value);
            if (!isNaN(page) && page >= 1 && page <= totalPages) {{
                goToPage(page);
                input.value = ''; // Clear input after navigation
            }} else {{
                alert(`Please enter a page number between 1 and ${{totalPages}}`);
            }}
        }}
        
        function clearFilters() {{
            document.getElementById('searchInput').value = '';
            document.getElementById('minPrice').value = '';
            document.getElementById('maxPrice').value = '';
            document.getElementById('tagFilter').value = '';
            document.getElementById('perPageSelect').value = '100';
            perPageLimit = '100';
            buyNowFilterActive = false;
            const buyNowBtn = document.getElementById('buyNowBtn');
            if (buyNowBtn) {{
                buyNowBtn.style.backgroundColor = '';
                buyNowBtn.style.fontWeight = '';
            }}
            filterDomains();
        }}
        
        function copyEmail(event, email) {{
            event.preventDefault();
            event.stopPropagation();
            navigator.clipboard.writeText(email).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '[OK] Copied';
                setTimeout(() => {{ btn.textContent = originalText; }}, 1500);
            }}).catch(err => {{
                console.error('Failed to copy:', err);
            }});
        }}
        
        function randomizeMarketplaceLinks() {{
            const container = document.querySelector('.marketplace-links');
            if (!container) return;
            
            const links = Array.from(container.querySelectorAll('a'));
            for (let i = links.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [links[i], links[j]] = [links[j], links[i]];
            }}
            
            container.innerHTML = '';
            links.forEach(link => container.appendChild(link));
        }}
    </script>
</body>
</html>'''
    
    return html


def check_requirements():
    """Check if required packages are installed and offer to install if missing"""
    missing = []
    optional_missing = []
    
    # Required packages
    try:
        import pandas
    except ImportError:
        missing.append('pandas')
    
    # Optional packages
    try:
        import deep_translator
    except ImportError:
        optional_missing.append('deep-translator')
    
    if missing:
        print("\n[X] Missing REQUIRED packages:")
        for pkg in missing:
            print(f"    - {pkg}")
        print("\nWould you like to install them now?")
        print("  1. Yes, install required packages")
        print("  2. No, exit")
        choice = input("\nYour choice [1/2]: ").strip()
        
        if choice == '1':
            import subprocess
            print("\n[INFO] Installing required packages...")
            for pkg in missing:
                print(f"  Installing {pkg}...")
                subprocess.run(['pip', 'install', pkg], check=True)
            print("\n[OK] Required packages installed!")
        else:
            print("\n[X] Cannot continue without required packages")
            sys.exit(1)
    
    if optional_missing:
        print("\n[!] Missing OPTIONAL packages (for translations):")
        for pkg in optional_missing:
            print(f"    - {pkg}")
        print("\nWould you like to install them?")
        print("  1. Yes, install optional packages")
        print("  2. Skip, continue without translation features")
        choice = input("\nYour choice [1/2]: ").strip()
        
        if choice == '1':
            import subprocess
            print("\n[INFO] Installing optional packages...")
            for pkg in optional_missing:
                print(f"  Installing {pkg}...")
                subprocess.run(['pip', 'install', pkg], check=True)
            print("\n[OK] Optional packages installed!")
        else:
            print("\n[INFO] Continuing without translation features...")

def main():
    # Check for required/optional packages
    check_requirements()
    
    print("HNS Portfolio Maker for timax.al")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        # No command-line arguments - show menu
        print("\n--- INTERACTIVE MODE ---\n")
        
        # Check if settings file exists
        settings_exists = (Path(__file__).parent / "portfolio-settings.json").exists()
        
        if settings_exists:
            print("Options:")
            print("  1. Run with portfolio-settings.json")
            print("  2. See 'help'")
            print("  3. Exit")
        else:
            print("Options:")
            print("  1. See 'help'")
            print("  2. Exit")
            print("\n[WARNING] Note: portfolio-settings.json not found in script directory")
        
        choice = input("\nEnter choice: ").strip()
        
        if settings_exists:
            if choice == '1':
                # Load and use settings
                settings = load_settings_if_exists()
                if settings:
                    input_paths = settings.get('csv_files', [])
                    include_all = settings.get('all', False)  # New: include all domains or only with price
                    auto_email = settings.get('email', '')  # Get email from settings if provided
                    include_descriptions = settings.get('include_descriptions', False)  # Load description setting
                    title = settings.get('title', 'HNS Portfolio')
                    output_filename = settings.get('output_filename', 'portfolio.html')
                    credits_file = settings.get('credits_file', '')  # Empty string = from settings, None = not from settings
                    if not input_paths:
                        print("\n[X] No csv_files specified in settings.json")
                        sys.exit(1)
                    
                    # Expand paths (files or directories)
                    print("\n[INFO] Expanding paths from settings...")
                    input_paths = expand_csv_paths(input_paths)
                    if not input_paths:
                        print("[X] No CSV files found after expanding paths")
                        sys.exit(1)
                    # We'll process settings below
                else:
                    print("\n[X] Failed to load settings")
                    sys.exit(1)
            elif choice == '2':
                show_help()
                sys.exit(0)
            elif choice == '3':
                print("\nExiting.")
                sys.exit(0)
            else:
                print("\n[X] Invalid choice. Exiting.")
                sys.exit(1)
        else:
            if choice == '1':
                show_help()
                sys.exit(0)
            elif choice == '2':
                print("\nExiting.")
                sys.exit(0)
            else:
                print("\n[X] Invalid choice. Exiting.")
                sys.exit(1)
    else:
        input_paths = sys.argv[1:]
        settings = None
        auto_email = None  # Will be prompted below if needed
        include_all = False  # Default for CLI mode (only priced domains for Bob/FW)
        include_descriptions = None  # Will be prompted
        title = None
        output_filename = None
        credits_file = None
    csv_files = []
    
    # Expand directories to CSV files
    for path in input_paths:
        if not os.path.exists(path):
            print(f"Warning: Path not found: {path}")
            continue
        found = find_csv_files(path, recursive=True)
        if found and os.path.isdir(path):
            print(f"[DIR] Found {len(found)} CSV file(s) in: {os.path.basename(path)}")
        csv_files.extend(found)
    
    if not csv_files:
        print("\n[X] No CSV files found!")
        sys.exit(1)
    
    print(f"\n[FILE] Processing {len(csv_files)} CSV file(s)\n")
    
    # Ask for auto-email (optional) - but only if not already provided from settings
    if auto_email is None:
        auto_email = input("Auto-email for priced domains (format: user+@gmail.com, or leave empty): ").strip()
    elif auto_email:
        print(f"[INFO] Using email from settings: {auto_email}")

    all_domains = []

    # Process all CSV files
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"Warning: File not found: {csv_file}")
            continue
        
        print(f"\nProcessing: {os.path.basename(csv_file)}")
        domains = process_csv(csv_file, auto_email=auto_email, include_all=include_all)
        print(f"  Found {len(domains)} domains")
        all_domains.extend(domains)
    
    if not all_domains:
        print("\nNo domains found in CSV files!")
        sys.exit(1)
    
    print(f"\nTotal domains: {len(all_domains)}")
    
    # Generate HTML - use settings if loaded, otherwise prompt
    if title is None:
        title = input("\nEnter page title (default: HNS Portfolio): ").strip()
        if not title:
            title = "HNS Portfolio"
    else:
        print(f"[INFO] Using title from settings: {title}")

    if output_filename is None:
        output_filename = input("Enter output filename (default: portfolio.html): ").strip()
        if not output_filename:
            output_filename = "portfolio.html"
    else:
        print(f"[INFO] Using output filename from settings: {output_filename}")
    if not output_filename.endswith('.html'):
        output_filename += '.html'

    # Ask for credits file - but only if not from settings (None means CLI mode, '' means from settings)
    if credits_file is None:
        credits_file = input("Enter credits HTML file path (or leave empty): ").strip()
    elif credits_file:
        print(f"[INFO] Using credits file from settings: {credits_file}")
    if credits_file and not os.path.exists(credits_file):
        print(f"Warning: Credits file not found: {credits_file}")
        credits_file = None

    # Ask if descriptions should be included
    if include_descriptions is None:
        include_desc = input("Include descriptions/translations in page? (y/N): ").strip().lower()
        include_descriptions = include_desc in ['y', 'yes']
    else:
        desc_status = "enabled" if include_descriptions else "disabled"
        print(f"[INFO] Descriptions/translations from settings: {desc_status}")
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent.parent / "HTML" / "sellhns" / "hns-tld"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename
    
    # Check if any domains have email (for info banner)
    has_email = any(d.get('email') for d in all_domains)
    plain_email = auto_email if auto_email and '+' not in auto_email else ''

    try:
        html_content = generate_html(all_domains, output_filename, title, credits_file, include_descriptions, has_email, plain_email)
        print(f"\n[INFO] HTML generated successfully ({len(html_content)} characters)")
        
        with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(html_content)
        
        print(f"[OK] Portfolio created: {output_path}")
    except Exception as e:
        print(f"\n[ERROR] Failed to generate portfolio: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    print(f"\nView at: file:///{output_path}")

if __name__ == "__main__":
    main()


