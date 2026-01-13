
import os

target_file = r'c:\Users\shrey\OneDrive\Desktop\oka\shell-lite\shell_lite\parser.py'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

search_str = """        first_expr = self.parse_expression()
        skip_formatted()
        if self.check('FOR'):"""

replace_str = """        first_expr = self.parse_expression()
        skip_formatted()
        
        if self.check('TO'):
            self.consume('TO')
            end_val = self.parse_expression()
            skip_formatted()
            self.consume('RBRACKET')
            node = Call('range', [first_expr, end_val])
            node.line = token.line
            return node

        if self.check('FOR'):"""

if search_str in content:
    new_content = content.replace(search_str, replace_str)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched parser.py")
else:
    print("Could not find search string. Trying flexible match.")
    # Try normalized newlines?
    # Or just print a nearby chunk to debug
    idx = content.find("first_expr = self.parse_expression()")
    if idx != -1:
         print(f"Found anchor at {idx}. Context:")
         print(repr(content[idx:idx+100]))
    else:
         print("Anchor not found.")
