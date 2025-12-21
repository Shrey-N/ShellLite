say "=== Verification Test ==="

# 1. Test 'when' as 'if'
x = 10
when x > 5
    say "PASS: 'when' works as 'if'"
else
    say "FAIL: 'when' condition failed"

# 2. Test 'greet' function (implicit call)
to greet name="World"
    say "Hello " + name

say "Testing implicit call:"
greet "Alice"
greet

# 3. Test 'when' as switch (legacy/standard check)
val = "test"
when val
    is "test"
        say "PASS: 'when' switch works"
    otherwise
        say "FAIL: 'when' switch failed"

say "=== Done ==="
