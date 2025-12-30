import os

# Create mock global folder package
global_dir = os.path.expanduser("~/.shell_lite/modules")
pkg_dir = os.path.join(global_dir, "pkg_folder")
if not os.path.exists(pkg_dir): os.makedirs(pkg_dir)

# Create main.shl inside
with open(os.path.join(pkg_dir, "main.shl"), 'w', encoding='utf-8') as f:
    f.write('say "Folder Package Loaded"')

# Create tests
with open('test_folder.shl', 'w', encoding='utf-8') as f:
    f.write('use "pkg_folder"')
    
with open('test_folder_alias.shl', 'w', encoding='utf-8') as f:
    f.write('use "pkg_folder" as pkg')

print("Folder test setup complete.")
