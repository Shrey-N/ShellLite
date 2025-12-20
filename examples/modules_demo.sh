# ShellLite Modules Demo
# Tests: env, args, path, color, re modules

say "=== ShellLite Modules Demo ==="
say ""

# --- Environment Module ---
use "env"
say "--- Environment Module ---"
say "PATH exists: " + str env.has "PATH"
say "HOME: " + str env.get "USERPROFILE"

# --- Path Module ---
use "path"
say ""
say "--- Path Module ---"
testpath = "C:/Users/test/documents/file.txt"
say "Path: {testpath}"
say "basename: " + path.basename testpath
say "dirname: " + path.dirname testpath
say "ext: " + path.ext testpath

# --- Args Module ---
use "args"
say ""
say "--- Args Module ---"
say "Arg count: " + str args.count()
say "All args: " + str args.all()

# --- Color Module ---
use "color"
say ""
say "--- Color Module ---"
say color.red "This is red!"
say color.green "This is green!"
say color.blue "This is blue!"
say color.yellow "This is yellow!"
say color.bold "This is bold!"

# --- Regex Module ---
use "re"
say ""
say "--- Regex Module ---"
text = "Hello 123 World 456"
say "Text: {text}"
say "match 'Hello': " + str re.match "Hello" text
say "findall digits: " + str re.findall "\\d+" text
say "replace digits with X: " + re.replace "\\d+" "X" text

say ""
say "=== All module tests passed! ==="
