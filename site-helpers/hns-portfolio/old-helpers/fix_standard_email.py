"""
Manual HTML Fix for Email Button Issue

When email has NO '+' sign (standard email like: user@gmail.com):
- Remove ALL @eml copy buttons from domains
- Update info message to show standard contact email
- Add email to footer/info section instead
"""
import re
import sys

def fix_standard_email_portfolio(input_path, standard_email, output_path=None):
    """Fix portfolio when using standard email (no '+' template)"""
    
    if output_path is None:
        output_path = input_path.replace('.html', '_STANDARD_EMAIL.html')
    
    print(f'Reading: {input_path}')
    print(f'Standard email (no "+"): {standard_email}')
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count original email buttons
    orig_buttons = len(re.findall(r'<button[^>]+class="copy-email-btn"[^>]*>', content))
    print(f'Original @eml buttons: {orig_buttons}')
    
    # FIX 1: Remove ALL @eml copy buttons (since email doesn't have '+')
    # Pattern: <button class="copy-email-btn" onclick="copyEmail(event, '...')">@eml</button>
    content = re.sub(
        r'<button[^>]+class="copy-email-btn"[^>]+onclick="copyEmail\([^)]+\)"[^>]*>@eml</button>',
        '',
        content
    )
    
    # Also remove from list view if present
    content = re.sub(
        r'<button[^>]+copy-email-btn[^>]*>[^<]*</button>',
        '',
        content
    )
    
    new_buttons = len(re.findall(r'<button[^>]+class="copy-email-btn"[^>]*>', content))
    print(f'Remaining @eml buttons: {new_buttons} (removed {orig_buttons - new_buttons})')
    
    # FIX 2: Update info message
    old_msg = 'Namebase/Shakestation domains have marketplace links. Non-custodial domains show copy-email buttons for enquiries.'
    new_msg = f'Namebase/Shakestation domains have marketplace links. For non-custodial domains, contact: <a href="mailto:{standard_email}" style="color: inherit; text-decoration: underline;">{standard_email}</a>'
    
    if old_msg in content:
        content = content.replace(old_msg, new_msg)
        print('[OK] Updated info message')
    else:
        # Try to find and update any similar message
        content = re.sub(
            r'Non-custodial domains show copy-email buttons for enquiries\.',
            f'For non-custodial domains, contact: <a href="mailto:{standard_email}">{standard_email}</a>',
            content
        )
        print('[OK] Updated info message (pattern match)')
    
    # FIX 3: Add email to footer if not present
    if '<footer>' in content and standard_email not in content.split('<footer>')[1].split('</footer>')[0]:
        # Add email to footer
        content = content.replace(
            '</footer>',
            f'<p style="margin-top: 1em;">Contact: <a href="mailto:{standard_email}">{standard_email}</a></p>\n</footer>'
        )
        print('[OK] Added email to footer')
    
    # FIX 4: Clean up empty contact divs (where email button was removed)
    # Pattern: <div class="domain-contact">💰 123</div> <- This is OK (has price)
    # Pattern: <div class="domain-contact"></div> <- This should be removed
    content = re.sub(
        r'<div class="domain-contact">\s*</div>',
        '',
        content
    )
    
    # Also clean up domain-contact divs that only have whitespace
    content = re.sub(
        r'<div class="domain-contact">\s+</div>',
        '',
        content
    )
    print('[OK] Cleaned up empty contact divs')
    
    # FIX 5: Update copyEmail function to show warning if somehow still called
    content = re.sub(
        r'(function copyEmail\(event, email\) \{)',
        r'''\1
            console.warn('copyEmail called but using standard email format');
            if (!'''' + standard_email + ''''.includes('+')) {
                alert('Please contact: ''' + standard_email + '''');
                return;
            }''',
        content
    )
    print('[OK] Updated copyEmail function with failsafe')
    
    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'\n[OK] Fixed HTML saved to: {output_path}')
    print(f'\nChanges made:')
    print(f'  - Removed {orig_buttons - new_buttons} @eml buttons')
    print(f'  - Updated info message to show standard email')
    print(f'  - Added failsafe to copyEmail function')
    print(f'  - Cleaned up empty contact divs')
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        print('\nUsage: python fix_standard_email.py <input.html> <email@address.com> [output.html]')
        print('\nExample:')
        print('  python fix_standard_email.py portfolio.html user@gmail.com')
        sys.exit(1)
    
    input_file = sys.argv[1]
    email = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = fix_standard_email_portfolio(input_file, email, output_file)
    sys.exit(0 if success else 1)
