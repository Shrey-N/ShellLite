
path = r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\interpreter.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Expand tabs to 4 spaces? Or just assume 4 spaces.
    # If line starts with tabs, convert to 4 spaces per tab.
    # If line starts with spaces, ensure multiple of 4?
    # Simple approach: replace \t with 4 spaces.
    new_line = line.replace('\t', '    ')
    new_lines.append(new_line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Indentation fixed (tabs to spaces).")
