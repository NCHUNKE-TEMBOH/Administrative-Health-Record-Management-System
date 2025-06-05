#!/usr/bin/env python3
"""
Simple test to check PulseCare static files and pages
"""

import os
import re
from datetime import datetime

def check_file_exists(filepath):
    """Check if a file exists and return basic info"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        return True, f"File exists ({size} bytes)"
    else:
        return False, "File not found"

def check_html_content(filepath):
    """Check HTML file for basic structure and 'coming soon' messages"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for basic HTML structure
        if '<html' not in content.lower():
            issues.append("Missing <html> tag")
        if '</html>' not in content.lower():
            issues.append("Missing </html> closing tag")
        if '<title>' not in content.lower():
            issues.append("Missing <title> tag")
        
        # Check for "coming soon" or "under development" messages
        coming_soon_patterns = [
            r'coming soon',
            r'under development',
            r'module is currently under development',
            r'this feature is coming soon'
        ]
        
        for pattern in coming_soon_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"Contains '{pattern}' message")
        
        return issues
        
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

def test_pulsecare_pages():
    """Test all PulseCare pages"""
    print("🏥 PulseCare Hospital Management System - Static File Testing")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define pages to test
    pages_to_test = {
        'Public Pages': [
            'static/index.html',
            'static/login.html',
            'static/signup.html',
            'static/about_us.html',
            'static/dashboard.html'
        ],
        'Admin Pages': [
            'static/admin/users.html',
            'static/admin/patients.html',
            'static/admin/health-records.html'
        ],
        'Doctor Pages': [
            'static/doctor/appointments.html',
            'static/doctor/patients.html',
            'static/doctor/prescriptions.html',
            'static/doctor/lab-tests.html',
            'static/doctor/medical-notes.html'
        ],
        'Nurse Pages': [
            'static/nurse/patients.html',
            'static/nurse/vital-signs.html',
            'static/nurse/assignments.html',
            'static/nurse/nursing-notes.html'
        ],
        'Lab Technician Pages': [
            'static/lab/tests.html',
            'static/lab/pending-tests.html',
            'static/lab/in-progress-tests.html',
            'static/lab/test-results.html',
            'static/lab/enter-results.html'
        ],
        'Pharmacist Pages': [
            'static/pharmacy/prescriptions.html',
            'static/pharmacy/dispense.html',
            'static/pharmacy/inventory.html',
            'static/pharmacy/history.html'
        ],
        'Patient Pages': [
            'static/patient/appointments.html',
            'static/patient/health-records.html',
            'static/patient/lab-results.html',
            'static/patient/prescriptions.html',
            'static/patient/vital-signs.html'
        ]
    }
    
    total_pages = 0
    pages_exist = 0
    pages_with_issues = 0
    pages_coming_soon = 0
    
    for category, pages in pages_to_test.items():
        print(f"\n📁 {category}")
        print("-" * 40)
        
        for page in pages:
            total_pages += 1
            exists, info = check_file_exists(page)
            
            if exists:
                pages_exist += 1
                print(f"✅ {os.path.basename(page)}: EXISTS")
                
                # Check HTML content
                issues = check_html_content(page)
                if issues:
                    pages_with_issues += 1
                    for issue in issues:
                        if 'coming soon' in issue.lower() or 'under development' in issue.lower():
                            pages_coming_soon += 1
                            print(f"   ⚠️  {issue}")
                        else:
                            print(f"   ❌ {issue}")
                else:
                    print(f"   ✅ HTML structure looks good")
            else:
                print(f"❌ {os.path.basename(page)}: {info}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total Pages Tested: {total_pages}")
    print(f"Pages Found: {pages_exist}")
    print(f"Pages Missing: {total_pages - pages_exist}")
    print(f"Pages with Issues: {pages_with_issues}")
    print(f"Pages with 'Coming Soon': {pages_coming_soon}")
    
    if pages_exist == total_pages:
        print("\n✅ All pages exist!")
    else:
        print(f"\n⚠️  {total_pages - pages_exist} pages are missing")
    
    if pages_coming_soon > 0:
        print(f"⚠️  {pages_coming_soon} pages still show 'coming soon' messages")
    else:
        print("✅ No 'coming soon' messages found!")
    
    # Check for PulseCare branding
    print(f"\n🏷️  BRANDING CHECK")
    print("-" * 30)
    
    branding_files = ['static/login.html', 'static/signup.html', 'static/index.html']
    pulsecare_count = 0
    
    for file in branding_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'PulseCare' in content:
                pulsecare_count += 1
                print(f"✅ {os.path.basename(file)}: Contains PulseCare branding")
            else:
                print(f"❌ {os.path.basename(file)}: Missing PulseCare branding")
    
    print(f"\nBranding Status: {pulsecare_count}/{len(branding_files)} files have PulseCare branding")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_pulsecare_pages()
