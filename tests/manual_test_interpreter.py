from src.ast_nodes import *
from src.interpreter import Interpreter
import sys
import os

# Add parent directory to path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_ast_execution():
    print("Testing Interpreter...")
    interpreter = Interpreter()

    # Test 1: 10 + 5
    # Code: print(10 + 5)
    print("\nTest 1: Arithmetic (10 + 5)")
    ast1 = Print(
        expression=BinOp(
            left=Number(10),
            op='+',
            right=Number(5)
        )
    )
    interpreter.visit(ast1)

    # Test 2: Variables
    # Code: 
    #   a = 20
    #   print(a)
    print("\nTest 2: Variables (a = 20; print a)")
    ast2 = [
        Assign(name='a', value=Number(20)),
        Print(expression=VarAccess(name='a'))
    ]
    for node in ast2:
        interpreter.visit(node)

    # Test 3: If statement
    # Code:
    #   if 5 > 2:
    #       print("5 is bigger")
    print("\nTest 3: If Statement (if 5 > 2)")
    ast3 = If(
        condition=BinOp(left=Number(5), op='>', right=Number(2)),
        body=[
            Print(expression=String("5 is bigger"))
        ]
    )
    interpreter.visit(ast3)

    # Test 4: For Loop
    # Code:
    #   for 3 in range:
    #       print("loop")
    print("\nTest 4: For Loop (3 iterations)")
    ast4 = For(
        count=Number(3),
        body=[
            Print(expression=String("loop"))
        ]
    )
    interpreter.visit(ast4)
    print("\nFinished.")

if __name__ == "__main__":
    test_ast_execution()
