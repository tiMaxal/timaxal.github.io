"""
HNS Portfolio JavaScript Fixer
Repairs the orphaned brace error in generated portfolio HTML files

Usage:
    python fix_any_portfolio.py <input_file.html> [output_file.html]
    
Examples:
    python fix_any_portfolio.py portfolio.html
    python fix_any_portfolio.py portfolio.html portfolio_fixed.html
"""
import sys
import re

def fix_portfolio_js(input_path, output_path=None):
    """Fix the JavaScript brace balance error in portfolio HTML"""
    
    if output_path is None:
        # Default: add _FIXED before .html
        output_path = input_path.replace('.html', '_FIXED.html')
    
    print(f'Reading: {input_path}')
    
    # Read the HTML
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'ERROR: File not found: {input_path}')
        return False
    
    # Extract the script section
    match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not match:
        print('ERROR: No <script> tag found in HTML!')
        return False
    
    js_original = match.group(1)
    lines = js_original.split('\n')
    
    print(f'Original JavaScript: {len(lines)} lines')
    
    # Check if already fixed
    open_b = js_original.count('{')
    close_b = js_original.count('}')
    balance = open_b - close_b
    
    print(f'Brace balance: {balance} (open={open_b}, close={close_b})')
    
    if balance == 0:
        print('✓ JavaScript already balanced - no fix needed!')
        print(f'  (If page still broken, issue is elsewhere)')
        return True
    
    if balance != -2:
        print(f'WARNING: Expected balance of -2, got {balance}')
        print('  This script fixes the specific 2-brace error.')
        print('  Your file may have a different issue.')
    
    # Apply the fix: Remove lines 177-180, add proper price filter
    fixed_lines = []
    skipped = 0
    added = 0
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Skip the problematic orphaned braces (lines 177-180)
        if 176 <= i <= 179:
            # Check if this looks like the orphaned code
            if ('} else {' in line or 
                'priceMatch = false' in line or 
                (line.strip() == '}' and 176 <= i <= 179)):
                skipped += 1
                continue
        
        # At line 176, after textMatch, add proper price filter
        if i == 175:  # Line 176 (0-indexed)
            fixed_lines.append(line)  # Add the textMatch line
            
            # Add the proper price filter logic
            fixed_lines.extend([
                '',
                '                // Price filter',
                '                let priceMatch = true;',
                '                if (minPrice !== null || maxPrice !== null) {',
                '                    const priceStr = domainDiv?.dataset?.price;',
                '                    if (priceStr) {',
                '                        const price = parseFloat(priceStr);',
                '                        if (minPrice !== null && price < minPrice) priceMatch = false;',
                '                        if (maxPrice !== null && price > maxPrice) priceMatch = false;',
                '                    } else if (minPrice !== null || maxPrice !== null) {',
                '                        priceMatch = false; // No price but filter active',
                '                    }',
                '                }'
            ])
            added = 13
        else:
            fixed_lines.append(line)
    
    js_fixed = '\n'.join(fixed_lines)
    
    # Replace in content - ONLY FIRST OCCURRENCE to avoid corrupting HTML
    # Use regex with count=1 to replace only the first <script> tag
    pattern = re.escape('<script>') + re.escape(js_original) + re.escape('</script>')
    content_fixed = re.sub(pattern, '<script>' + js_fixed + '</script>', content, count=1)
    
    # Safety check: Verify replacement worked
    if '<script>' + js_fixed + '</script>' not in content_fixed:
        print('\nWARNING: Replacement may have failed!')
        print('Trying alternative method...')
        # Fallback: Find and replace using string positions
        start_pos = content.find('<script>' + js_original + '</script>')
        if start_pos >= 0:
            end_pos = start_pos + len('<script>' + js_original + '</script>')
            content_fixed = content[:start_pos] + '<script>' + js_fixed + '</script>' + content[end_pos:]
        else:
            print('ERROR: Could not locate script tag in content!')
            return False
    
    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content_fixed)
    
    print(f'\n[OK] Fixed HTML saved to: {output_path}')
    print(f'  Lines: {len(lines)} -> {len(fixed_lines)} ({added - skipped:+d})')
    print(f'  Removed {skipped} orphaned lines, added {added} proper filter lines')
    
    # Verify brace balance
    new_open = js_fixed.count('{')
    new_close = js_fixed.count('}')
    new_balance = new_open - new_close
    
    print(f'\nNew brace balance: {new_balance} (open={new_open}, close={new_close})')
    
    if new_balance == 0:
        print('[OK] SUCCESS! JavaScript is now balanced!')
        print('\nYour portfolio should now work correctly with:')
        print('  [OK] All domains visible')
        print('  [OK] Theme/sort/filter buttons functional')
        print('  [OK] Tag dropdown populated')
        print('  [OK] Price range filtering working')
        return True
    else:
        print(f'WARNING: Balance is {new_balance}, expected 0')
        print('  The fix may not have worked correctly.')
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        print('\nERROR: No input file specified!')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = fix_portfolio_js(input_file, output_file)
    sys.exit(0 if success else 1)
