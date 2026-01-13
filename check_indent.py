
path = r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'class Interpreter' in line:
        print(f"{i+1}: {repr(line)}")
    if 'def _builtin_filter' in line:
        print(f"{i+1}: {repr(line)}")
    if 'def visit_Call' in line:
        print(f"{i+1}: {repr(line)}")
    if 'def _builtin_upper' in line:
        print(f"{i+1}: {repr(line)}")
