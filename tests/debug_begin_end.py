import sys
sys.path.insert(0, '.')
from shell_lite.lexer import Lexer
from shell_lite.parser_gbp import GeometricBindingParser
from shell_lite.interpreter import Interpreter

# Test with no-argument function
source = '''to greet
begin
say "Hello World"
end

greet
'''

lex = Lexer(source)
tokens = lex.tokenize()
parser = GeometricBindingParser(tokens)
ast = parser.parse()

print('=== EXECUTION ===')
interp = Interpreter()
for node in ast:
    interp.visit(node)
