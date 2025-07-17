#!/usr/bin/env python3
"""Quick fix for Unicode issues in CLI"""
import re

def replace_unicode_in_file(file_path):
    """Replace Unicode emojis with text equivalents"""
    
    # Unicode emoji mappings
    replacements = {
        '📋': '[INFO]',
        '❌': '[ERROR]',
        '🆔': '[ID]',
        '🎭': '[MODE]', 
        '👥': '[USERS]',
        '📊': '[STATS]',
        '📅': '[DATE]',
        '💭': '[TOPIC]',
        '💡': '[TIP]',
        '🤖': '[AGENT]',
        '👤': '[USER]',
        '✅': '[OK]',
        '⚠️': '[WARN]',
        '🔍': '[SEARCH]',
        '📝': '[NOTE]',
        '🚀': '[START]',
        '🔥': '[HOT]',
        '⭐': '[STAR]',
        '🎯': '[TARGET]',
        '🔧': '[CONFIG]',
        '📁': '[FOLDER]',
        '📄': '[FILE]',
        '🌟': '[NEW]',
        '🔄': '[REFRESH]',
        '💾': '[SAVE]',
        '🗂️': '[ARCHIVE]'
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace emojis
        for emoji, replacement in replacements.items():
            content = content.replace(emoji, replacement)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Fixed Unicode issues in {file_path}")
        
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")

if __name__ == "__main__":
    replace_unicode_in_file("src/ams_db/cli/main.py")
