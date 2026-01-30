import sys
sys.path.insert(0, '.')
from shell_lite.lexer import Lexer
from shell_lite.parser_gbp import GeometricBindingParser
from shell_lite.interpreter import Interpreter

source = '''
# Test begin/end with function
to greet name
begin
    say "Hello " + name
end

greet "World"

# Test begin/end with if statement
x = 10
if x > 5
begin
    say "x is greater than 5"
end

# Test nested begin/end
if x > 0
begin
    if x > 5
    begin
        say "nested begin/end works!"
    end
end

# Test mixing begin/end with indentation (define with begin/end, body with indent)
to compute n
begin
    result = n * 2
    return result
end

answer = compute 21
say "The answer is " + answer
'''

lex = Lexer(source)
tokens = lex.tokenize()
parser = GeometricBindingParser(tokens)
ast = parser.parse()

interp = Interpreter()
for node in ast:
    interp.visit(node)
