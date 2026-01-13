"""
Fix Portfolio Button Issues
- Theme button text disappearing
- Show/hide descriptions button missing
- Email button logic (only show when email has '+')
"""
import re
import sys

def fix_portfolio_buttons(input_path, output_path=None):
    """Fix button visibility and email logic issues"""
    
    if output_path is None:
        output_path = input_path.replace('.html', '_BUTTONS_FIXED.html')
    
    print(f'Reading: {input_path}')
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JavaScript section
    js_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not js_match:
        print('ERROR: No <script> tag found!')
        return False
    
    js_original = js_match.group(1)
    js_fixed = js_original
    
    # FIX 1: Theme button text disappearing
    # The issue is likely in cycleTheme() function overwriting button element
    # Make sure we update textContent, not replace the button
    
    # Find and fix the cycleTheme function
    cycle_theme_pattern = r'(function cycleTheme\(\) \{.*?)(const themeBtn = document\.getElementById\(\'themeBtn\'\);)'
    if re.search(cycle_theme_pattern, js_fixed, re.DOTALL):
        # Add null check
        js_fixed = re.sub(
            r'(function cycleTheme\(\) \{)\s*(const themeBtn = document\.getElementById\(\'themeBtn\'\);)',
            r'\1\n            const themeBtn = document.getElementById(\'themeBtn\');\n            if (!themeBtn) return;',
            js_fixed
        )
        print('[OK] Added theme button null check')
    
    # FIX 2: Ensure applyTheme preserves button
    apply_theme_pattern = r'(function applyTheme\(\).*?)(\bthemeBtn\.textContent = )'
    if re.search(apply_theme_pattern, js_fixed, re.DOTALL):
        js_fixed = re.sub(
            r'(function applyTheme\(\) \{)',
            r'\1\n            const themeBtn = document.getElementById(\'themeBtn\');\n            if (!themeBtn) return;',
            js_fixed,
            count=1
        )
        print('[OK] Added applyTheme button check')
    
    # FIX 3: Add DOMContentLoaded initialization for theme button
    if 'DOMContentLoaded' in js_fixed and 'applyTheme' in js_fixed:
        # Make sure applyTheme is called after DOM loads
        if "addEventListener('DOMContentLoaded'" in js_fixed:
            print('[OK] DOMContentLoaded already present')
        else:
            # Add it before the closing script tag
            js_fixed = js_fixed.rstrip() + '''

        // Initialize theme on page load
        document.addEventListener('DOMContentLoaded', () => {
            applyTheme();
            showSection('all-names');
        });
'''
            print('[OK] Added DOMContentLoaded handler')
    
    # Replace JavaScript in content
    content = content.replace('<script>' + js_original + '</script>', 
                             '<script>' + js_fixed + '</script>')
    
    # FIX 4: Make show/hide descriptions button visible
    # Check if button exists in HTML
    if 'toggle-descriptions' in content or 'toggleDescriptions' in content:
        # Button might be hidden by CSS, ensure it's visible
        content = re.sub(
            r'(<button[^>]+id=["\']toggle-descriptions["\'][^>]*)(style="display:\s*none;")',
            r'\1',
            content
        )
        
        # Ensure button is in the button container
        if '#toggle-descriptions' not in content:
            # Add CSS to make it visible
            content = re.sub(
                r'(\.buttons-container[^}]*\{[^}]*\})',
                r'\1\n.buttons-container #toggle-descriptions { display: inline-block; }',
                content
            )
        print('[OK] Made descriptions button visible')
    else:
        print('⚠ Show/hide descriptions button not found in HTML')
    
    # FIX 5: Email button logic - only show @eml when email has '+'
    # Find the format_domain_link section in Python script, but for HTML we need to check
    # if email buttons are conditionally rendered
    
    # Check current email button pattern
    email_btn_matches = re.findall(r'copyEmail\(event,\s*[\'"]([^\'"]*)[\'"]\)', content)
    if email_btn_matches:
        print(f'[OK] Found {len(email_btn_matches)} email copy buttons')
        
        # Check if any emails have '+' 
        has_plus = any('+' in email for email in email_btn_matches)
        has_no_plus = any('+' not in email and '@' in email for email in email_btn_matches)
        
        if has_no_plus:
            print(f'⚠ Found emails WITHOUT + sign: {[e for e in email_btn_matches[:3] if "+" not in e]}')
            print('  These should not have @eml buttons visible')
            print('  (This needs to be fixed in the Python generator script)')
    
    # FIX 6: Update info message about email buttons
    # Find the info message and update it based on email format
    info_pattern = r'Namebase/Shakestation domains have marketplace links\.\s*Non-custodial domains show copy-email buttons for enquiries\.'
    
    if re.search(info_pattern, content):
        # Check if we have standard email (no +) vs template email (has +)
        has_template_email = any('+' in email for email in email_btn_matches) if email_btn_matches else False
        
        if not has_template_email and email_btn_matches:
            # Standard email - update message
            replacement_msg = 'Namebase/Shakestation domains have marketplace links. Non-custodial domains: contact via standard email (see footer).'
            content = re.sub(info_pattern, replacement_msg, content)
            print('[OK] Updated info message for standard email')
        else:
            print('[OK] Info message OK (template email format detected)')
    
    # Save fixed content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'\n[OK] Fixed HTML saved to: {output_path}')
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        print('\nUsage: python fix_portfolio_buttons.py <input.html> [output.html]')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = fix_portfolio_buttons(input_file, output_file)
    sys.exit(0 if success else 1)
