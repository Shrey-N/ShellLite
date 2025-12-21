# ShellLite Standard Library Demo
# Tests: String, List, File operations and Regex

say "=== ShellLite Standard Library Demo ==="
say ""

# --- String Operations ---
say "--- String Operations ---"
text = "  Hello, World!  "
say "Original: '{text}'"
say "trim: '" + trim text + "'"
say "upper: " + upper "hello"
say "lower: " + lower "HELLO"
say "replace: " + replace "hello world" "world" "ShellLite"

words = split "apple,banana,cherry" ","
say "split: " + str words
say "join: " + join words " | "

say "startswith 'hello' 'he': " + str startswith "hello" "he"
say "endswith 'hello' 'lo': " + str endswith "hello" "lo"
say "find 'hello' 'll': " + str find "hello" "ll"

say ""
say "--- List Operations ---"
nums = [3, 1, 4, 1, 5, 9, 2, 6]
say "Original: " + str nums
say "sorted: " + str sort nums
say "reversed: " + str reverse nums
say "slice 2 5: " + str slice nums 2 5
say "contains 4: " + str contains nums 4
say "index of 5: " + str index nums 5

say ""
say "--- Math Functions ---"
say "abs -5: " + str abs -5
say "min 3 7: " + str min 3 7
say "max 3 7: " + str max 3 7
say "pow 2 8: " + str pow 2 8
say "round 3.7: " + str round 3.7

say ""
say "--- Type Functions ---"
say "typeof 42: " + typeof 42
say "typeof 'hello': " + typeof "hello"
say "typeof [1,2,3]: " + typeof [1, 2, 3]
say "typeof yes: " + typeof yes

say ""
say "=== All stdlib tests passed! ==="
