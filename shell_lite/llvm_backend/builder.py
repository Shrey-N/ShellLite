import llvmlite.binding as llvm
from .codegen import LLVMCompiler
from ..lexer import Lexer
from ..parser import Parser
import os

def build_llvm(filename: str):
    print(f"Compiling {filename} with LLVM Backend...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()

    # 1. Parse
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statements = parser.parse()

    # 2. Codegen (Generate IR)
    compiler = LLVMCompiler()
    module = compiler.compile(statements)
    
    # 3. Print IR
    llvm_ir = str(module)
    print("\n--- Generated LLVM IR ---")
    print(llvm_ir)
    print("-------------------------\n")

    # 4. Save IR to file
    ll_filename = os.path.splitext(filename)[0] + ".ll"
    with open(ll_filename, 'w') as f:
        f.write(llvm_ir)
    print(f"[SUCCESS] Generated LLVM IR: {ll_filename}")
    
    # 5. Try Native Compilation (Optional)
    # Note: Binding seems unstable, so we skip it for now and recommend `clang`.
    print("\nTo compile to executable, you can use Clang:")
    print(f"  clang {ll_filename} -o {os.path.splitext(filename)[0]}.exe")
    
    """
    try:
        print("Initializing LLVM...")
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        print("LLVM Initialized.")

        print("Creating Target...")
        target = llvm.Target.from_default_triple()
        print(f"Target Triple: {target}")
        target_machine = target.create_target_machine()
        
        # ... (rest of binding code)
    except Exception as e:
        print(f"Native binding skipped due to: {e}")
    """

