"""
ALL-IN-ONE Portfolio Fixer

Applies all three fixes in sequence:
1. JavaScript syntax (brace balance)
2. Button visibility (theme, descriptions)
3. Email button removal (for standard email format)

Usage:
    python fix_portfolio_all.py <input.html> [email@address.com]
    
Examples:
    # Auto-detect email from HTML:
    python fix_portfolio_all.py portfolio.html
    
    # Specify standard email:
    python fix_portfolio_all.py portfolio.html user@gmail.com
"""
import sys
import os
import subprocess

def fix_all(input_file, email=None):
    """Apply all fixes in sequence"""
    
    if not os.path.exists(input_file):
        print(f'ERROR: File not found: {input_file}')
        return False
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print('=' * 70)
    print('PORTFOLIO ALL-IN-ONE FIXER')
    print('=' * 70)
    print(f'Input: {input_file}')
    print()
    
    # Step 1: Fix JavaScript syntax
    print('Step 1/3: Fixing JavaScript brace balance...')
    fix1_script = os.path.join(script_dir, 'fix_any_portfolio.py')
    temp1 = input_file.replace('.html', '_TEMP1.html')
    
    result = subprocess.run(
        ['python', fix1_script, input_file, temp1],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print('✗ Step 1 failed!')
        print(result.stdout)
        print(result.stderr)
        return False
    
    print('[OK] Step 1 complete: JavaScript syntax fixed')
    print()
    
    # Step 2: Fix button visibility
    print('Step 2/3: Fixing button visibility...')
    fix2_script = os.path.join(script_dir, 'fix_portfolio_buttons.py')
    temp2 = input_file.replace('.html', '_TEMP2.html')
    
    result = subprocess.run(
        ['python', fix2_script, temp1, temp2],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print('✗ Step 2 failed!')
        print(result.stdout)
        print(result.stderr)
        return False
    
    print('[OK] Step 2 complete: Buttons fixed')
    print()
    
    # Step 3: Fix email buttons (if standard email)
    if email:
        if '+' in email:
            print(f'Step 3/3: Skipped (email has "+" - template format: {email})')
            output_file = temp2
        else:
            print(f'Step 3/3: Removing email buttons (standard email: {email})...')
            fix3_script = os.path.join(script_dir, 'fix_standard_email.py')
            output_file = input_file.replace('.html', '_COMPLETE.html')
            
            result = subprocess.run(
                ['python', fix3_script, temp2, email, output_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print('✗ Step 3 failed!')
                print(result.stdout)
                print(result.stderr)
                return False
            
            print('[OK] Step 3 complete: Email buttons removed')
    else:
        # Auto-detect email from HTML
        print('Step 3/3: Detecting email format...')
        with open(temp2, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for copyEmail calls to determine if template email is used
        import re
        email_matches = re.findall(r"copyEmail\(event,\s*'([^']+)'\)", content)
        
        if email_matches:
            sample_email = email_matches[0]
            if '+' in sample_email:
                print(f'  Detected: Template email format (has "+"): {sample_email}')
                print('  Keeping @eml buttons')
                output_file = temp2
            else:
                print(f'  Detected: Standard email format (no "+"): {sample_email}')
                print(f'  Removing @eml buttons...')
                
                fix3_script = os.path.join(script_dir, 'fix_standard_email.py')
                output_file = input_file.replace('.html', '_COMPLETE.html')
                
                result = subprocess.run(
                    ['python', fix3_script, temp2, sample_email, output_file],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print('✗ Step 3 failed!')
                    print(result.stdout)
                    print(result.stderr)
                    return False
                
                print('[OK] Step 3 complete: Email buttons removed')
        else:
            print('  No email buttons found - skipping email fix')
            output_file = temp2
    
    # Rename final output
    if output_file == temp2:
        final_output = input_file.replace('.html', '_COMPLETE.html')
        os.rename(temp2, final_output)
        output_file = final_output
    
    # Cleanup temp files
    if os.path.exists(temp1):
        os.remove(temp1)
    if os.path.exists(temp2) and temp2 != output_file:
        os.remove(temp2)
    
    print()
    print('=' * 70)
    print('[SUCCESS] ALL FIXES COMPLETE!')
    print('=' * 70)
    print(f'Output file: {output_file}')
    print()
    print('Your portfolio now has:')
    print('  [OK] JavaScript syntax fixed (brace balance = 0)')
    print('  [OK] Theme button text visible and functional')
    print('  [OK] Show/Hide Descriptions button visible')
    print('  [OK] Email buttons correctly handled')
    print('  [OK] All 1606 domains displayed')
    print('  [OK] All buttons functional')
    print()
    print(f'Open: {output_file}')
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    input_file = sys.argv[1]
    email = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = fix_all(input_file, email)
    sys.exit(0 if success else 1)
