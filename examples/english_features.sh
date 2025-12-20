# ShellLite Advanced English Features Test

say "=== Testing New Features ==="

# --- Stop (break) and Skip (continue) ---
say ""
say "--- Stop and Skip ---"
i = 0
repeat 10 times
    i = i + 1
    if i == 3
        skip
    if i == 7
        stop
    say "Count: " + str i

# --- Unless (negative if) ---
say ""
say "--- Unless ---"
done = no
unless done
    say "Not done yet!"

# --- Until loop ---
say ""
say "--- Until ---"
x = 0
until x == 3
    x = x + 1
    say "x = " + str x

# --- Repeat ---
say ""
say "--- Repeat ---"
repeat 3 times
    say "Hello!"

# --- Pattern Matching (when/is/otherwise) ---
say ""
say "--- Pattern Matching ---"
color = "red"
when color
    is "red"
        say "Stop!"
    is "green"
        say "Go!"
    otherwise
        say "Unknown color"

# --- Error handling ---
say ""
say "--- Custom Errors ---"
try
    error "Something went wrong!"
catch e
    say "Caught: " + e

# --- Execute dynamic code ---
say ""
say "--- Execute ---"
code = "say 'Dynamic code!'"
execute code

# --- Unique (sets) ---
say ""
say "--- Unique ---"
nums = [1, 1, 2, 2, 3, 3]
say "Original: " + str len nums
result = unique nums
say "Unique count: " + str len result

# --- first/last/empty ---
say ""
say "--- First/Last/Empty ---"
items = ["apple", "banana", "cherry"]
say "First: " + first items
say "Last: " + last items

say ""
say "=== All English features tested! ==="
