#!/usr/bin/env python3
"""
Find all pages with "coming soon" messages in medicare
"""

import os
import re

def find_coming_soon_pages():
    """Find all HTML files with coming soon messages"""
    coming_soon_pages = []
    static_dir = "static"
    
    # Walk through all HTML files
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for coming soon patterns
                    patterns = [
                        r'coming soon',
                        r'under development',
                        r'module is currently under development',
                        r'this feature is coming soon',
                        r'showComingSoon\(\)'
                    ]
                    
                    found_patterns = []
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            found_patterns.append(pattern)
                    
                    if found_patterns:
                        coming_soon_pages.append({
                            'file': filepath,
                            'patterns': found_patterns
                        })
                        
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return coming_soon_pages

if __name__ == "__main__":
    print("🔍 Finding pages with 'Coming Soon' messages...")
    print("=" * 50)
    
    pages = find_coming_soon_pages()
    
    if pages:
        print(f"Found {len(pages)} pages with 'Coming Soon' messages:\n")
        for page in pages:
            print(f"📄 {page['file']}")
            for pattern in page['patterns']:
                print(f"   - Contains: {pattern}")
            print()
    else:
        print("✅ No pages with 'Coming Soon' messages found!")
    
    print("=" * 50)
    print(f"Total pages to fix: {len(pages)}")
