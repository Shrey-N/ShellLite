
import sys
import glob
import os

files = [
    r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\parser.py',
    r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\lexer.py',
    r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter.py',
    r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\main.py',
    r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\ast_nodes.py',
    r'c:\Users\shrey\OneDrive\Desktop\oka\tests_suite\repro_issues.shl'
]

for path in files:
    try:
        with open(path, 'rb') as f:
            content = f.read()

        if b'\x00' in content:
            print(f"Null bytes found in {path}! Fixing...")
            new_content = content.replace(b'\x00', b'')
            with open(path, 'wb') as f:
                f.write(new_content)
            print(f"Fixed {path}.")
        else:
            print(f"No null bytes in {path}.")
    except Exception as e:
        print(f"Error checking {path}: {e}")
