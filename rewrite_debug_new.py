
path_src = r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter_backup.py'
path_dst = r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter_new.py'

with open(path_src, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "'filter':" in line or "'map':" in line or "'reduce':" in line:
        continue
    if "def __init__(self):" in line:
         new_lines.append(line)
         new_lines.append("        print('DEBUG: STEP 0 - START INIT')\n")
         new_lines.append("        self.global_env = Environment()\n")
         new_lines.append("        print('DEBUG: STEP 1 - Env Created')\n")
    elif "self.current_env = self.global_env" in line:
         new_lines.append(line)
         new_lines.append("        print('DEBUG: STEP 2 - Context Set')\n")
    elif "self.builtins = {" in line:
         new_lines.append("        print('DEBUG: STEP 3 - Start Builtins')\n")
         new_lines.append(line)
    elif "self._init_std_modules()" in line:
         new_lines.append("        print('DEBUG: STEP 4 - Init Std Modules')\n")
         new_lines.append(line)
         new_lines.append("        print('DEBUG: STEP 5 - DONE')\n")
    else:
         new_lines.append(line)

with open(path_dst, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Rewrite interpreter_new.py success.")
