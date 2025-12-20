print "--- Interactive Layout Test ---"
print "What is your name?"
name = input "> "
print "Hello " + name
print "Enter a number to double:"
str_num = input
# Note: Input returns string, simple language doesn't have int() cast yet in parsed code logic, 
# but let's see if we can do implicit cast or just string repetition
print "You entered: " + str_num
# casting isn't implemented in the language standard library yet, but we can verify input works.
print "Done."
