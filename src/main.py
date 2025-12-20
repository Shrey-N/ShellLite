import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

def execute_source(source: str, interpreter: Interpreter):
    lines = source.split('\n')
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        statements = parser.parse()
        
        for stmt in statements:
            interpreter.visit(stmt)
    except Exception as e:
        if hasattr(e, 'line') and e.line > 0:
            print(f"Error on line {e.line}:")
            if 0 <= e.line-1 < len(lines):
                print(f"  {lines[e.line-1].strip()}")
            print(f"{type(e).__name__}: {e}")
        else:
            print(f"Error: {e}")

def run_file(filename: str):
    with open(filename, 'r') as f:
        source = f.read()
    interpreter = Interpreter()
    execute_source(source, interpreter)

def run_repl():
    interpreter = Interpreter()
    print("Welcome to ShellLite REPL!")
    print("Maintained by Shrey Naithani")
    print("Type 'exit' to quit.")
    
    buffer = []
    indent_level = 0
    
    while True:
        try:
            prompt = "... " if indent_level > 0 else ">>> "
            line = input(prompt)
            
            if line.strip() == "exit":
                break
                
            if not line:
                if indent_level > 0:
                    # Execute buffered block
                    source = "\n".join(buffer)
                    execute_source(source, interpreter)
                    buffer = []
                    indent_level = 0
                continue

            if line.strip().startswith(("if ", "for ")):
                indent_level = 1
                buffer.append(line)
                continue
                
            if indent_level > 0:
                if line.startswith("    ") or line.startswith("\t"):
                    buffer.append(line)
                else:
                    # Dedent / End of block
                    source = "\n".join(buffer)
                    execute_source(source, interpreter)
                    buffer = []
                    indent_level = 0
                    # Execute current line as new statement
                    if line.strip():
                        execute_source(line, interpreter)
                continue

            # Standard single line execution
            execute_source(line, interpreter)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            buffer = []
            indent_level = 0

def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()

if __name__ == "__main__":
    main()
