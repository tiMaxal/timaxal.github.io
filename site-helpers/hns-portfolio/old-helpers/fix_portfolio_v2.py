import re

# Path to the HTML file
html_path = r'E:\STORE\DOCS\text\personal\tdwebsite\timax.al-githubio\HTML\sellhns\portfolio.html'
output_path = r'E:\STORE\DOCS\text\personal\tdwebsite\timax.al-githubio\HTML\sellhns\portfolio_FIXED.html'

# Read the HTML
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the script section
match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if not match:
    print('Error: No <script> tag found!')
    exit(1)

js_original = match.group(1)
lines = js_original.split('\n')

print(f'Original: {len(lines)} lines')

# Fix the specific problem: Remove lines 177-180 which are orphaned closing braces
# Line 177:                     } else {
# Line 178:                         priceMatch = false;
# Line 179:                     }
# Line 180:                 }

# Instead, we need to add proper price filtering logic after line 176
# We'll rebuild the function correctly

fixed_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    
    # Skip the problematic lines 177-180 (indices 176-179)
    if 176 <= i <= 179:
        continue
    
    # At line 176, after adding textMatch, add the missing price filter logic
    if i == 175:  # Line 176 (0-indexed = 175)
        fixed_lines.append(line)  # Add the textMatch line
        # Now add the proper price filter logic
        fixed_lines.append('')
        fixed_lines.append('                // Price filter')
        fixed_lines.append('                let priceMatch = true;')
        fixed_lines.append('                if (minPrice !== null || maxPrice !== null) {')
        fixed_lines.append('                    const priceStr = domainDiv?.dataset?.price;')
        fixed_lines.append('                    if (priceStr) {')
        fixed_lines.append('                        const price = parseFloat(priceStr);')
        fixed_lines.append('                        if (minPrice !== null && price < minPrice) priceMatch = false;')
        fixed_lines.append('                        if (maxPrice !== null && price > maxPrice) priceMatch = false;')
        fixed_lines.append('                    } else if (minPrice !== null || maxPrice !== null) {')
        fixed_lines.append('                        priceMatch = false; // No price but filter active')
        fixed_lines.append('                    }')
        fixed_lines.append('                }')
    else:
        fixed_lines.append(line)

js_fixed = '\n'.join(fixed_lines)

# Replace in content
content_fixed = content.replace('<script>' + js_original + '</script>', 
                               '<script>' + js_fixed + '</script>')

# Save
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print(f'Fixed HTML saved to: {output_path}')
print(f'New line count: {len(fixed_lines)} lines ({len(fixed_lines) - len(lines):+d})')

# Count braces
open_b = js_fixed.count('{')
close_b = js_fixed.count('}')
balance = open_b - close_b
print(f'Brace count: {{ = {open_b}, }} = {close_b}, balance = {balance}')

if balance == 0:
    print('✓ Brace balance is correct!')
else:
    print(f'✗ WARNING: Brace balance is still {balance}')

# Try to validate with Node.js if available
print('\nValidating JavaScript with Node.js...')
import subprocess
try:
    # Create a validation script
    val_script = """
const fs = require('fs');
const html = fs.readFileSync(%r, 'utf8');
const match = html.match(/<script>([\\s\\S]*?)<\\/script>/);
if (match) {
    try {
        eval(match[1]);
        console.log('✓ JavaScript is VALID! All functions execute without errors.');
    } catch (e) {
        console.log('✗ JavaScript ERROR:', e.message);
        process.exit(1);
    }
}
""" % output_path
    
    result = subprocess.run(
        ['node', '-e', val_script],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(result.stdout.strip())
    if result.stderr:
        print('Stderr:', result.stderr)
    if result.returncode == 0:
        print('\n✓✓✓ SUCCESS! Portfolio is now functional!')
except Exception as e:
    print(f'Could not validate with Node.js: {e}')
