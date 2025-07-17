#!/usr/bin/env python3
"""
Fix import paths in test files
"""
import os
import glob

# Standard import fix for tests
IMPORT_FIX = '''import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

'''

def fix_test_file(file_path):
    """Fix imports in a test file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it already has the sys.path fix
    if 'sys.path.insert' in content:
        print(f"✅ {file_path} already has import fix")
        return
    
    # Find where to insert the import fix
    lines = content.split('\n')
    
    # Find the first src.ams_db import
    insert_line = None
    for i, line in enumerate(lines):
        if 'from src.ams_db' in line:
            insert_line = i
            break
    
    if insert_line is None:
        print(f"⚠️ No src.ams_db imports found in {file_path}")
        return
    
    # Insert the import fix before the first src.ams_db import
    lines.insert(insert_line, IMPORT_FIX.strip())
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Fixed imports in {file_path}")

def main():
    """Fix all test files"""
    test_files = glob.glob('tests/*.py')
    
    for test_file in test_files:
        if test_file.endswith('__init__.py'):
            continue
        fix_test_file(test_file)
    
    print(f"\n🎉 Fixed imports in {len(test_files)} test files!")

if __name__ == '__main__':
    main()
