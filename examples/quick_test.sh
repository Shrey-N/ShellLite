# Quick test of new features
say "=== Quick Test ==="

# Constants
const PI = 3.14
say "PI = " + str PI

# Ternary
x = 10
result = x > 5 ? "big" : "small"
say "Ternary: " + result

# Lambda
double = fn n => n * 2
val = double 5
say "Lambda double 5 = " + str val

# List comprehension
nums = [1, 2, 3, 4, 5]
squares = [n * n for n in nums]
say "Squares: " + str squares

# Spread
a = [1, 2]
b = [3, 4]
c = [...a, ...b]
say "Spread: " + str c

# For-in
say "For-in:"
for i in range 1 4
    say "  " + str i

# String ops
say "Upper: " + upper "hello"
say "Lower: " + lower "WORLD"

# Modulo
m = 10 % 3
say "10 % 3 = " + str m

# Modules
use "math"
say "math.pi = " + str math.pi

use "color"
say color.green "Success!"

say "=== All tests passed! ==="
