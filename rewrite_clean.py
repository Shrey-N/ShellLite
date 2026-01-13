
path_backup = r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter_backup.py'
path_target = r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter.py'

with open(path_backup, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "'filter':" in line or "'map':" in line or "'reduce':" in line:
        continue
    if "def __init__(self):" in line:
         new_lines.append(line)
         new_lines.append("        print('DEBUG: VERSION 2 LOADED')\n")
    else:
         new_lines.append(line)

with open(path_target, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("interpreter.py re-written clean.")
