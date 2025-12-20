say "--- Full Language Test ---"

# 1. Else/Elif
say "Testing Control Flow:"
val = 50
if val > 100
    say "Huge"
elif val > 40
    say "Medium (Correct)"
else
    say "Small"

# 2. Booleans
say "Testing Booleans:"
is_happy = yes
is_sad = no

if is_happy is yes
    say "I am happy!"

if is_sad is no
    say "I am not sad!"

# 3. Floats
say "Testing Floats:"
pi = 3.14
r = 2
area = pi * r * r
say "Area should be ~12.56: " + area

# 4. Lists & Len
say "Testing Lists:"
items = [10, 20, 30]
count = len items
say "List has " + count + " items"
say items

# 5. Functions & Models (Regression Test)
to double x
    return x * 2

d = double 5
say "Double 5 is " + d

say "All systems go."
