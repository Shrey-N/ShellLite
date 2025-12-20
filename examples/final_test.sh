# Final test of all features
say "=== Final Test ==="

# Always block
say "1. Always block:"
try
    say "  Trying..."
    error "oops"
catch e
    say "  Caught: " + e
always
    say "  Always runs!"

# Repeat
say "2. Repeat:"
repeat 2 times
    say "  Hi!"

# When/is/otherwise  
say "3. Pattern matching:"
x = "b"
when x
    is "a"
        say "  A!"
    is "b"
        say "  B!"
    otherwise
        say "  Other"

# Unless
say "4. Unless:"
done = no
unless done
    say "  Still going!"

# Until
say "5. Until:"
n = 0
until n == 2
    n = n + 1
    say "  n = " + str n

# Stop/Skip
say "6. Stop/Skip:"
repeat 5 times
    say "  Loop"
    stop

# Execute
say "7. Execute:"
execute "say '  Dynamic!'"

# Lambdas
say "8. Lambda:"
double = fn x => x * 2
say "  double 5 = " + str double 5

say "=== All tests passed! ==="
