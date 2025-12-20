say "--- OS Capability Test ---"

# 1. Run Command
say "Running 'ver' command..."
v = run "ver"
say "Version info: " + v

# 2. File Write
say "Writing test file..."
write "test_os.txt" "OS Test Content"

# 3. File Read
say "Reading test file..."
c = read "test_os.txt"
if c == "OS Test Content"
    say "Read verification SUCCESS"
else
    say "Read verification FAILED: " + c

say "Test Complete"
