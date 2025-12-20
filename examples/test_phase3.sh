say "Testing Phase 3 Features"
say ""

say "1. OS Command"
# Note: 'run' is a function. 'run "cmd"' is valid call syntax.
# Windows uses 'echo', make sure to run on Windows cmd/powershell
out = run "echo Hello from Shell"
say "Output: " + out

say ""
say "2. File I/O"
path = "test_io.txt"
success = write path "Hello File"
say "Write success: " + success
content = read path
say "Read content: " + content

# Cleanup using OS command (Windows 'del')
run "del " + path

say ""
say "3. JSON"
# Create dict with string keys
obj = {"a": 1, "b": 2}
json_str = json_stringify obj
say "JSON String: " + json_str

parsed = json_parse json_str
say "Parsed a: " + parsed.a
