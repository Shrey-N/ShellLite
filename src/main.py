import sys
import os
import shutil
import urllib.request
import zipfile
import io
import subprocess
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
        print(f"Exception: {e}")

def run_file(filename: str):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return
    with open(filename, 'r') as f:
        source = f.read()
    interpreter = Interpreter()
    execute_source(source, interpreter)

def run_repl():
    interpreter = Interpreter()
    print("\n" + "="*40)
    print("  ShellLite REPL - English Syntax")
    print("="*40)
    print("Version: v0.03.3 | Made by Shrey Naithani")
    print("Commands: Type 'exit' to quit, 'help' for examples.")
    print("Note: Terminal commands (like 'shl install') must be run in CMD/PowerShell, not here.")
    
    buffer = []
    indent_level = 0
    
    while True:
        try:
            prompt = "... " if indent_level > 0 else ">>> "
            line = input(prompt)
            
            if line.strip() == "exit":
                break
            
            # Support line continuation with \
            if line.endswith("\\"):
                buffer.append(line[:-1])
                indent_level = 1
                continue
            if line.strip() == "help":
                print("\nShellLite Examples:")
                print('  say "Hello World"')
                print('  tasks is a list            # Initialize an empty list')
                print('  add "Buy Milk" to tasks    # Add items to the list')
                print('  display(tasks)             # View the list')
                print('  \\                          # Tip: Use \\ at the end of a line for multi-line typing')
                continue

            if line.strip().startswith("shl"):
                print("! Hint: You are already INSIDE ShellLite. You don't need to type 'shl' here.")
                print("! To run terminal commands, exit this REPL first.")
                continue

            if not line:
                if indent_level > 0:
                    source = "\n".join(buffer)
                    execute_source(source, interpreter)
                    buffer = []
                    indent_level = 0
                continue

            if line.strip().endswith(":"):
                indent_level = 1
                buffer.append(line)
            elif indent_level > 0 and (line.startswith(" ") or line.startswith("\t")):
                buffer.append(line)
            else:
                if indent_level > 0:
                     source = "\n".join(buffer)
                     execute_source(source, interpreter)
                     buffer = []
                     indent_level = 0
                
                if line.strip():
                    execute_source(line, interpreter)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            buffer = []
            indent_level = 0

def install_globally():
    """Performs the global PATH installation."""
    print("\n" + "="*50)
    print("  ShellLite Global Installer")
    print("="*50)
    
    install_dir = os.path.join(os.environ['LOCALAPPDATA'], 'ShellLite')
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)
    
    target_exe = os.path.join(install_dir, 'shl.exe')
    current_path = sys.executable
    
    # If not running as EXE (e.g. py script), we can't 'install' the script easily as shl.exe
    is_frozen = getattr(sys, 'frozen', False)
    
    try:
        if is_frozen:
            shutil.copy2(current_path, target_exe)
        else:
            print("Error: Installation requires the shl.exe file.")
            return

        # Add to PATH (User level)
        ps_cmd = f'$oldPath = [Environment]::GetEnvironmentVariable("Path", "User"); if ($oldPath -notlike "*ShellLite*") {{ [Environment]::SetEnvironmentVariable("Path", "$oldPath;{install_dir}", "User") }}'
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
        
        print(f"\n[SUCCESS] ShellLite is now installed!")
        print(f"Location: {install_dir}")
        print("\nACTION REQUIRED:")
        print("1. Close this terminal window.")
        print("2. Open a NEW terminal.")
        print("3. Type 'shl' to verify.")
        print("="*50 + "\n")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"Installation failed: {e}")

def compile_file(filename: str):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    print(f"Compiling {filename}...")
    
    with open(filename, 'r') as f:
        source = f.read()
        
    try:
        from .compiler import Compiler
        from .parser import Parser
        from .lexer import Lexer
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        statements = parser.parse()
        
        compiler = Compiler()
        python_code = compiler.compile(statements)
        
        output_file = filename.replace('.shl', '.py')
        if output_file == filename: output_file += ".py"
        
        with open(output_file, 'w') as f:
            f.write(python_code)
            
        print(f"[SUCCESS] Transpiled to {output_file}")
        
        # Optional: Compile to EXE using PyInstaller
        # This requires 'pyinstaller' to be installed in the user's environment.
        try:
            import PyInstaller.__main__
            print("Building Executable with PyInstaller...")
            PyInstaller.__main__.run([
                output_file,
                '--onefile',
                '--name', os.path.splitext(os.path.basename(filename))[0],
                '--log-level', 'WARN'
            ])
            print(f"[SUCCESS] Built {os.path.splitext(os.path.basename(filename))[0]}.exe")
        except ImportError:
            print("Note: PyInstaller not found. Generated .py file only.")
            print("To build .exe, run: pip install pyinstaller")

    except Exception as e:
        print(f"Compilation Failed: {e}")


def self_install_check():
    """Checks if shl is in PATH, if not, offer to install it."""
    # Simple check: is shl.exe in a known Global path?
    # Or just check if 'shl' works in shell
    res = subprocess.run(["where", "shl"], capture_output=True, text=True)
    if "ShellLite" not in res.stdout:
        print("\nShellLite is not installed globally.")
        choice = input("Would you like to install it so 'shl' works everywhere? (y/n): ").lower()
        if choice == 'y':
            install_globally()

def show_help():
    print("""
ShellLite - The English-Like Programming Language
Usage:
  shl <filename.shl>    Run a ShellLite script
  shl                   Start the interactive REPL
  shl help              Show this help message
  shl compile <file>    Compile a script to an executable
  shl install           Install ShellLite globally to your system PATH

For documentation, visit: https://github.com/Shrey-N/ShellDesk
""")

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "compile" or cmd == "build":
            if len(sys.argv) > 2:
                compile_file(sys.argv[2])
            else:
                print("Usage: shl compile <filename>")
        elif cmd == "help" or cmd == "--help" or cmd == "-h":
            show_help()
        elif cmd == "install":
            if len(sys.argv) > 2:
                # Install a package
                print(f"Installing package {sys.argv[2]}...")
            else:
                # Install ShellLite itself
                install_globally()
        else:
            run_file(sys.argv[1])
    else:
        # No args - trigger install check, then REPL
        self_install_check()
        run_repl()

if __name__ == "__main__":
    main()
