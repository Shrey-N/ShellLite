
# RE-READ ORIGINAL FILE CONTENT TO ENSURE CONSISTENCY
with open(r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter_backup.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert print at __init__
if "def __init__(self):" in content:
    content = content.replace("def __init__(self):", 
    "def __init__(self):\n        print('DEBUG: Loading LOCAL Interpreter')\n        print(f'DEBUG: dir(self) = {dir(self)}')")

with open(r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)
