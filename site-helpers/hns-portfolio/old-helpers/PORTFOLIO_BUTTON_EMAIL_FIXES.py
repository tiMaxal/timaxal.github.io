"""
HNS Portfolio Generator - Button & Email Fixes

Issues Fixed:
1. Theme button text disappearing (DOMContentLoaded timing)
2. Show/hide descriptions button missing from button container
3. Email @eml buttons showing even when email has no '+' (should be hidden)
4. Info message shows wrong text when standard email (no '+') is used

This file documents the fixes needed in hns-portfolio-maker.py
"""

# ============================================================================
# FIX 1: Show/Hide Descriptions Button - Make Visible
# ============================================================================
"""
Location: HTML template section where buttons are generated
Current: Button exists but may be hidden or not in button container
Fix: Ensure button is always visible and in the .buttons-container
"""

FIX_1_BUTTON_HTML = '''
<div class="buttons-container">
    <button id="themeBtn" onclick="cycleTheme()">☀️ Light</button>
    <button id="zoom-in">Zoom +</button>
    <button id="zoom-out">Zoom -</button>
    <button id="sort-tlds">Sort TLDs</button>
    <button id="toggle-view">📊 Grid / 📋 List</button>
    <button id="toggle-descriptions" style="display: inline-block;">Show/Hide Descriptions</button>
    <button id="clear-filters">Clear Filters</button>
</div>
'''

# Add this CSS to ensure button is visible:
FIX_1_CSS = '''
.buttons-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: flex-end;
}

.buttons-container button {
    display: inline-block !important;  /* Force visibility */
    padding: 8px 16px;
    background-color: rgba(52, 4, 244, 0.8);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    white-space: nowrap;
}
'''

# ============================================================================
# FIX 2: Theme Button Text Disappearing
# ============================================================================
"""
Location: JavaScript cycleTheme() and applyTheme() functions
Current: Button text disappears after page loads
Fix: Ensure button element exists before updating, add proper initialization
"""

FIX_2_JAVASCRIPT = '''
// Theme cycling (Light -> Dark -> Black)
let currentTheme = 0; // 0=light, 1=dark, 2=black

function cycleTheme() {
    const themeBtn = document.getElementById('themeBtn');
    if (!themeBtn) {
        console.error('Theme button not found!');
        return;
    }
    
    currentTheme = (currentTheme + 1) % 3;
    localStorage.setItem('theme', currentTheme.toString());
    applyTheme();
}

function applyTheme() {
    const themeBtn = document.getElementById('themeBtn');
    if (!themeBtn) return;
    
    document.body.classList.remove('dark-theme', 'black-theme');
    
    switch(currentTheme) {
        case 0: // Light
            themeBtn.textContent = '☀️ Light';
            break;
        case 1: // Dark
            document.body.classList.add('dark-theme');
            themeBtn.textContent = '🌙 Dark';
            break;
        case 2: // Black
            document.body.classList.add('black-theme');
            themeBtn.textContent = '⚫ Black';
            break;
    }
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    // Restore saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme !== null) {
        currentTheme = parseInt(savedTheme);
    }
    applyTheme();
    
    // Show default section
    showSection('all-names');
    
    // Populate tag filter dropdown
    populateTagFilter();
});
'''

# ============================================================================
# FIX 3: Email Button Logic - Only Show When Email Has '+'
# ============================================================================
"""
Location: format_domain_link() method in Python script
Current: @eml buttons show for all emails
Fix: Only show copy button when email contains '+' (template format)
      For standard emails (no '+'), show contact info in footer instead
"""

FIX_3_PYTHON_CODE = '''
def format_domain_link(self, row):
    name = row['name']
    unicode_val = str(row.get('unicode', ''))
    source = row.get('source', 'nb')
    email = row.get('email', '')
    price = row.get('price', '')
    descript = str(row.get('descript-IDNA', ''))
    translate = str(row.get('translate-IDNA', ''))
    
    # Check if email is template format (has '+') vs standard format
    has_template_email = '+' in email if email else False
    
    # ... existing code for unicode display ...
    
    # Build contact parts
    contact_parts = []
    if price:
        contact_parts.append(f"💰 {price}")
    
    # Only show copy button if email has '+' (template format)
    if email and has_template_email:
        copy_btn = f'<button class="copy-email-btn" onclick="copyEmail(event, \\'{email}\\')" title="Copy {email}">@eml</button>'
        contact_parts.append(copy_btn)
    # If standard email (no '+'), it should be in footer, not per-domain
    
    # ... rest of existing code ...
'''

# ============================================================================
# FIX 4: Info Message Based on Email Format
# ============================================================================
"""
Location: HTML info section generation in Python script
Current: Always shows "copy-email buttons for enquiries"
Fix: Check email format and show appropriate message
"""

FIX_4_INFO_MESSAGE = '''
# In the HTML generation section:
def generate_info_message(self):
    """Generate appropriate info message based on email format"""
    
    # Check portfolio settings for email format
    settings = self.load_settings()
    auto_email = settings.get('auto_email', '')
    
    if '+' in auto_email:
        # Template email format - copy buttons will be shown
        return """
        <div class="info-message">
            <p><strong>How to purchase:</strong></p>
            <p>• Namebase/Shakestation domains: Click domain name to view on marketplace</p>
            <p>• Non-custodial domains: Click <code>@eml</code> button to copy contact email</p>
            <p>• Email format: Each domain has unique email address for easy tracking</p>
        </div>
        """
    else:
        # Standard email format - contact via footer/general email
        return f"""
        <div class="info-message">
            <p><strong>How to purchase:</strong></p>
            <p>• Namebase/Shakestation domains: Click domain name to view on marketplace</p>
            <p>• Non-custodial domains: Contact via email: <a href="mailto:{auto_email}">{auto_email}</a></p>
            <p>• Include domain name in your enquiry</p>
        </div>
        """
'''

# ============================================================================
# IMPLEMENTATION CHECKLIST
# ============================================================================
"""
In hns-portfolio-maker.py:

[ ] 1. Find button container HTML generation (around line 600-650)
       - Add toggle-descriptions button with inline-block style
       - Ensure all buttons are in buttons-container div

[ ] 2. Find CSS section (around line 650-900)
       - Add .buttons-container button { display: inline-block !important; }
       - Verify buttons-container has proper z-index: 1000

[ ] 3. Find cycleTheme() function (around line 1070-1095)
       - Add null check: if (!themeBtn) return;
       - Add console.error for debugging

[ ] 4. Find applyTheme() function (around line 1095-1115)
       - Add null check at start: if (!themeBtn) return;

[ ] 5. Find DOMContentLoaded handler (around line 1095-1120)
       - Ensure applyTheme() is called
       - Ensure showSection('all-names') is called
       - Ensure populateTagFilter() is called

[ ] 6. Find format_domain_link() method (around line 800-950)
       - Add: has_template_email = '+' in email if email else False
       - Wrap email button in: if email and has_template_email:

[ ] 7. Find info message generation (may need to add this section)
       - Add generate_info_message() method
       - Call it when building HTML
       - Use dynamic message based on email format

[ ] 8. Test thoroughly:
       - Theme button text stays visible on page load
       - Theme button cycles through Light/Dark/Black
       - Show/Hide Descriptions button visible and functional
       - With '+' email: @eml buttons show, copy works
       - Without '+' email: no @eml buttons, general email in footer/info
       - Info message matches email format
"""

# ============================================================================
# TESTING SCENARIOS
# ============================================================================
"""
Test Case 1: Template Email (with '+')
  Settings: "auto_email": "user+@gmail.com"
  Expected:
    ✓ @eml buttons visible on domains
    ✓ Click copies domain-specific email (user+domainname@gmail.com)
    ✓ Info message: "Click @eml button to copy contact email"

Test Case 2: Standard Email (no '+')
  Settings: "auto_email": "user@gmail.com"
  Expected:
    ✓ NO @eml buttons on domains
    ✓ General email shown in info section or footer
    ✓ Info message: "Contact via email: user@gmail.com"

Test Case 3: No Email
  Settings: "auto_email": ""
  Expected:
    ✓ NO @eml buttons
    ✓ No email-related info message
    ✓ Only marketplace links for nb/ss domains

Test Case 4: Theme Button
  Expected:
    ✓ Button visible on page load with text "☀️ Light"
    ✓ Click cycles: Light -> Dark -> Black -> Light
    ✓ Text updates on each click
    ✓ Theme persists across page reloads

Test Case 5: Descriptions Button
  Expected:
    ✓ Button visible in button container
    ✓ Click toggles descriptions visibility
    ✓ Works in both grid and list views
"""

print(__doc__)
print("\nFixes documented. Apply these changes to hns-portfolio-maker.py")
print("Then regenerate portfolio and test all scenarios.")
