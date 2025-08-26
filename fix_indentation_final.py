#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix the final indentation issue in uwu_cli.py
"""

def fix_uwu_cli():
    """Fix the indentation error in uwu_cli.py"""
    
    # Read the file
    with open('uwu_cli.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the problematic indentation
    old_text = """            except ImportError:
                # Fallback to basic file completion
            try:
                dir_path = os.path.dirname(
                    text) if os.path.dirname(text) else '.'
                base_name = os.path.basename(text)

                if os.path.exists(dir_path):
                    for item in os.listdir(dir_path):
                        if item.startswith(base_name):
                            full_path = os.path.join(dir_path, item)
                            if os.path.isdir(full_path):
                                completions.append(full_path + os.sep)
                            else:
                                completions.append(full_path)
            except:
                pass"""
    
    new_text = """            except ImportError:
                # Fallback to basic file completion
                try:
                    dir_path = os.path.dirname(
                        text) if os.path.dirname(text) else '.'
                    base_name = os.path.basename(text)

                    if os.path.exists(dir_path):
                        for item in os.listdir(dir_path):
                            if item.startswith(base_name):
                                full_path = os.path.join(dir_path, item)
                                if os.path.isdir(full_path):
                                    completions.append(full_path + os.sep)
                                else:
                                    completions.append(full_path)
                except:
                    pass"""
    
    # Replace the text
    fixed_content = content.replace(old_text, new_text)
    
    # Write the fixed content back
    with open('uwu_cli.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Fixed indentation issue in uwu_cli.py")

if __name__ == "__main__":
    fix_uwu_cli() 