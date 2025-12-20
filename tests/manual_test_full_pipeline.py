import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def run_test(name, code):
    print(f"\n--- Test: {name} ---")
    print(f"Code:\n{code}")
    print("Output:")
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # print(f"DEBUG Tokens: {tokens}") # Uncomment to debug tokens
        
        parser = Parser(tokens)
        ast_nodes = parser.parse()
        # print(f"DEBUG Nodes: {ast_nodes}") # Uncomment to debug AST
        
        interpreter = Interpreter()
        results = []
        for node in ast_nodes:
            res = interpreter.visit(node)
            results.append(res)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def main():
    # Test 1: Arithmetic Implicit Print
    run_test("Arithmetic", "10 + 20")

    # Test 2: Strings
    run_test("Strings", "'Hello' + ' ' + 'World'")

    # Test 3: Assignment & Vars
    run_test("Variables", """
a = 50
a + 10
""")

    # Test 4: If Statement
    run_test("If Statement", """
x = 10
if x == 10
    print "x is 10"
if x > 5
    print "x is big"
""")

    # Test 5: For Loop
    run_test("For Loop", """
for 3 in range
    print "repeating"
""")

    # Test 6: Complex Indentation
    run_test("Complex Indentation", """
if 1 == 1
    print "Layer 1"
    if 2 == 2
        print "Layer 2"
    print "Back to Layer 1"
""")

if __name__ == "__main__":
    main()
