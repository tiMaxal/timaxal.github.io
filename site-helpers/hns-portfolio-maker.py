#!/usr/bin/env python3
"""
HNS Portfolio Maker for timax.al
Generates HTML portfolio pages from Namebase/Shakestation CSV exports
Styled to match timax.al theme with 3-way theme switcher
"""

import pandas as pd
import os
import sys
from pathlib import Path
import codecs
import re

def detect_csv_source(filepath):
    """Detect CSV source type from headers"""
    try:
        df = pd.read_csv(filepath, nrows=1)
        headers = [h.lower() for h in df.columns.tolist()]
        
        if 'extra.domain' in headers or 'extra.action' in headers:
            return 'nb-tr'
        elif 'domain' in headers and 'for_sale' in headers:
            return 'ss-tld'
        elif 'name' in headers and 'tags' in headers:
            return 'nb-tld'
        return 'unknown'
    except Exception as e:
        print(f"Error detecting source: {e}")
        return 'unknown'

def process_csv(filepath):
    """Process CSV and return list of domain dictionaries"""
    source_type = detect_csv_source(filepath)
    domains = []
    
    try:
        df = pd.read_csv(filepath)
        
        if source_type == 'ss-tld':
            # Only include domains marked for_sale=True
            df = df[df['for_sale'] == True]
            
        # Handle different column names
        if 'name' in df.columns:
            domain_col = 'name'
        elif 'domain' in df.columns:
            domain_col = 'domain'
        elif 'extra.domain' in df.columns:
            domain_col = 'extra.domain'
        else:
            print(f"Warning: No domain column found in {os.path.basename(filepath)}")
            return domains
        
        for _, row in df.iterrows():
            domain = {
                'name': row[domain_col],
                'unicode': row.get('unicode', ''),
                'descript': row.get('descript-IDNA', ''),
                'tags': row.get('tags', 'All Names'),
                'source': 'ss' if source_type.startswith('ss') else 'nb'
            }
            domains.append(domain)
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return domains

def format_domain_link(domain):
    """Format domain as HTML link with appropriate marketplace"""
    name = domain['name']
    unicode_val = str(domain.get('unicode', ''))
    source = domain.get('source', 'nb')
    
    if source == 'ss':
        base_url = f"https://shakestation.io/domain/{name}"
    else:
        base_url = f"https://www.namebase.io/domains/{name}"
    
    # Handle punycode domains
    if name.startswith('xn--'):
        if unicode_val and unicode_val.lower() != 'nan' and unicode_val.strip():
            try:
                unicode_bytes = codecs.decode(unicode_val, 'unicode_escape')
                unicode_char = unicode_bytes.encode('latin-1').decode('utf-8')
            except:
                unicode_char = unicode_val
            return f'<a href="{base_url}" target="_blank" rel="noreferrer">{unicode_char} <span class="puny">({name})</span></a>'
        else:
            return f'<a href="{base_url}" target="_blank" rel="noreferrer">{name}</a>'
    else:
        return f'<a href="{base_url}" target="_blank" rel="noreferrer">{name}</a>'

def generate_html(domains, output_filename="portfolio.html", title="HNS Portfolio"):
    """Generate HTML with timax.al theming"""
    
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
    
    # Sort tags: 'All Names' first, then alphabetical
    tags_sorted = ['All Names'] + sorted(set(tags_dict.keys()) - {'All Names'})
    
    # Generate navigation links
    nav_links = []
    for tag in tags_sorted:
        section_id = tag.lower().replace(' ', '-')
        nav_links.append(f'<button class="tag-button" onclick="showSection(\'{section_id}\')">{tag}</button>')
    
    # Generate tag sections
    sections = []
    for tag in tags_sorted:
        section_id = tag.lower().replace(' ', '-')
        domain_links = [f'<div class="domain-item">{format_domain_link(d)}</div>' 
                       for d in tags_dict[tag]]
        sections.append(f'''
        <div id="{section_id}" class="tag-section">
            <h3>{tag}</h3>
            <div class="domain-grid">
                {''.join(domain_links)}
            </div>
        </div>
        ''')
    
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
        
        .theme-switcher {{
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
        }}
        
        .theme-switcher:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        }}
        
        body.dark-theme .theme-switcher {{
            background-color: rgba(153, 221, 255, 0.8);
            color: #003366;
        }}
        
        body.black-theme .theme-switcher {{
            background-color: rgba(255, 255, 255, 0.8);
            color: #000000;
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
        
        .tag-navigation {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
            padding: 20px;
            background-color: rgba(52, 4, 244, 0.1);
            border-radius: 10px;
        }}
        
        body.dark-theme .tag-navigation {{
            background-color: rgba(153, 221, 255, 0.1);
        }}
        
        body.black-theme .tag-navigation {{
            background-color: rgba(255, 255, 255, 0.1);
        }}
        
        .tag-button {{
            padding: 8px 16px;
            background-color: rgba(52, 4, 244, 0.15);
            color: inherit;
            border: 2px solid currentColor;
            border-radius: 8px;
            cursor: pointer;
            font-family: inherit;
            font-size: 0.95em;
            transition: all 0.3s ease;
        }}
        
        .tag-button:hover {{
            background-color: rgba(52, 4, 244, 0.3);
            transform: translateY(-2px);
        }}
        
        body.dark-theme .tag-button {{
            background-color: rgba(153, 221, 255, 0.15);
        }}
        
        body.dark-theme .tag-button:hover {{
            background-color: rgba(153, 221, 255, 0.3);
        }}
        
        body.black-theme .tag-button {{
            background-color: rgba(255, 255, 255, 0.15);
        }}
        
        body.black-theme .tag-button:hover {{
            background-color: rgba(255, 255, 255, 0.3);
        }}
        
        .tag-section {{
            display: none;
            margin: 30px 0;
        }}
        
        .tag-section.active {{
            display: block;
        }}
        
        .tag-section h3 {{
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
        
        .footer {{
            margin-top: 50px;
            padding-top: 30px;
            text-align: center;
            border-top: 2px solid currentColor;
        }}
    </style>
    <link rel="stylesheet" href="../../site-helpers/site-nav.css?v=2">
    <script src="../../site-helpers/theme-switcher.js?v=2"></script>
    <script src="../../site-helpers/footer-loader.js?v=2"></script>
    <script src="../../site-helpers/site-nav.js?v=2"></script>
</head>
<body>
    <button id="themeBtn" class="theme-switcher" onclick="cycleTheme()">☀️ Light</button>
    
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search domains..." onkeyup="searchDomains()">
        </div>
        
        <div class="tag-navigation">
            {''.join(nav_links)}
        </div>
        
        {''.join(sections)}
        
        <div id="footer-container"></div>
    </div>
    
    <script>
        // Show first section by default
        document.addEventListener('DOMContentLoaded', function() {{
            showSection('all-names');
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
        
        function searchDomains() {{
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const items = document.querySelectorAll('.domain-item');
            
            items.forEach(item => {{
                const text = item.textContent.toLowerCase();
                if (text.includes(filter)) {{
                    item.style.display = '';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>'''
    
    return html

def main():
    print("HNS Portfolio Maker for timax.al")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python hns-portfolio-maker.py <csv_file1> [csv_file2] ...")
        print("\nOr drag CSV files onto this script")
        sys.exit(1)
    
    csv_files = sys.argv[1:]
    all_domains = []
    
    # Process all CSV files
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"Warning: File not found: {csv_file}")
            continue
        
        print(f"\nProcessing: {os.path.basename(csv_file)}")
        domains = process_csv(csv_file)
        print(f"  Found {len(domains)} domains")
        all_domains.extend(domains)
    
    if not all_domains:
        print("\nNo domains found in CSV files!")
        sys.exit(1)
    
    print(f"\nTotal domains: {len(all_domains)}")
    
    # Generate HTML
    title = input("\nEnter page title (default: HNS Portfolio): ").strip()
    if not title:
        title = "HNS Portfolio"
    
    output_filename = input("Enter output filename (default: portfolio.html): ").strip()
    if not output_filename:
        output_filename = "portfolio.html"
    if not output_filename.endswith('.html'):
        output_filename += '.html'
    
    # Determine output path
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "HTML" / "sellhns"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename
    
    html_content = generate_html(all_domains, output_filename, title)
    
    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ Portfolio created: {output_path}")
    print(f"\nView at: file:///{output_path}")

if __name__ == "__main__":
    main()
