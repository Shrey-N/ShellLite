import os

# Clean up
if os.path.exists('test_global.shl'): os.remove('test_global.shl')
if os.path.exists('test_implicit.shl'): os.remove('test_implicit.shl')

# Write clean UTF-8 files
with open('test_global.shl', 'w', encoding='utf-8') as f:
    f.write('use "test_mod.shl"')
    
with open('test_implicit.shl', 'w', encoding='utf-8') as f:
    f.write('use "test_mod"')

# Fix global module
global_dir = os.path.expanduser("~/.shell_lite/modules")
if not os.path.exists(global_dir): os.makedirs(global_dir)
global_mod = os.path.join(global_dir, "test_mod.shl")
if os.path.exists(global_mod): os.remove(global_mod)
with open(global_mod, 'w', encoding='utf-8') as f:
    f.write('say "Global Module Loaded"')

print("Test files created.")
