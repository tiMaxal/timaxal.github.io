import re

# Path to the HTML file
html_path = r'E:\STORE\DOCS\text\personal\tdwebsite\timax.al-githubio\HTML\sellhns\portfolio.html'
output_path = r'E:\STORE\DOCS\text\personal\tdwebsite\timax.al-githubio\HTML\sellhns\portfolio_fixed.html'

# Read the HTML
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the script section
match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if not match:
    print('Error: No <script> tag found!')
    exit(1)

js_original = match.group(1)

# Fix the JavaScript
js_fixed = js_original

# The most common error: extra closing braces at end of switch statements
# Pattern: }  } } -> } }
js_fixed = re.sub(r'}\s+}\s+}(\s+)', r'} }\1', js_fixed)

# Pattern: }} } -> } }
js_fixed = re.sub(r'}}\s+}', r'} }', js_fixed)

# Replace in content
content_fixed = content.replace('<script>' + js_original + '</script>', 
                               '<script>' + js_fixed + '</script>')

# Save
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print(f'Fixed HTML saved to: {output_path}')

# Count braces
open_b = js_fixed.count('{')
close_b = js_fixed.count('}')
print(f'Brace count: {{ = {open_b}, }} = {close_b}, balance = {open_b - close_b}')

# Try to validate with Node.js if available
import subprocess
try:
    result = subprocess.run(
        ['node', '-e', f'''
        const fs = require('fs');
        const html = fs.readFileSync('{output_path.replace(chr(92), chr(92)+chr(92))}', 'utf8');
        const match = html.match(/<script>([\\s\\S]*?)<\\/script>/);
        if (match) {{
            try {{
                eval(match[1]);
                console.log('✓ JavaScript is valid!');
            }} catch (e) {{
                console.log('✗ JavaScript ERROR:', e.message);
                process.exit(1);
            }}
        }}
        '''],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(result.stdout)
    if result.stderr:
        print('Stderr:', result.stderr)
except Exception as e:
    print(f'Could not validate with Node.js: {e}')
