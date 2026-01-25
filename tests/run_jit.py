import sys
import os
import time
import ctypes
import llvmlite.binding as llvm
try:
    from llvmlite.binding.orcjit import create_lljit_compiler, JITLibraryBuilder
except ImportError:
    # Fallback if not exposed directly
    import llvmlite.binding.orcjit as orc
    create_lljit_compiler = orc.create_lljit_compiler
    JITLibraryBuilder = orc.JITLibraryBuilder

# Add parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shell_lite.lexer import Lexer
from shell_lite.parser_gbp import GeometricBindingParser
from shell_lite.llvm_backend.codegen import LLVMCompiler

def compile_and_run_jit(source_code):
    # 1. Initialize LLVM
    # llvm.initialize() # Deprecated/Failing in 0.46
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    
    # 2. Parse (GBP)
    start_compile = time.perf_counter()
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    ast = GeometricBindingParser(tokens).parse()
    
    # 3. Codegen
    compiler = LLVMCompiler()
    ir_module = compiler.compile(ast)
    llvm_ir = str(ir_module)
    
    start_jit = time.perf_counter()
    
    # 4. Create OrcJIT Engine
    lljit = create_lljit_compiler()
    
    # 5. Build Library
    builder = JITLibraryBuilder()
    builder.add_ir(llvm_ir)
    
    # 6. Link
    # Note: "main" in our IR is usually just "main".
    # We define a library name.
    tracker = builder.link(lljit, "shell_lite_lib")
    
    # 7. Lookup 'main'
    # OrcJIT usually requires mangled names? C names are usually keys.
    # Our function is named "main".
    try:
        addr = tracker["main"]
    except KeyError:
        # Maybe underscore prefix on Windows?
        try:
             addr = tracker["_main"]
        except KeyError:
             print("Error: Could not find 'main' symbol.")
             return 0, 0, -1

    jit_time = time.perf_counter() - start_jit
    
    # 8. Run
    cfunc = ctypes.CFUNCTYPE(ctypes.c_int)(addr)
    
    start_run = time.perf_counter()
    res = cfunc()
    run_time = time.perf_counter() - start_run
    
    return start_jit - start_compile, run_time, res

if __name__ == "__main__":
    # Test code: Sum 10M (Heavy loop)
    # Python Loop Speed for 10M is roughly 0.5s - 1s in pure python loops?
    code = """
    sum = 0
    i = 0
    count = 10000000
    while i < count:
        sum = sum + 1
        i = i + 1
    print sum
    """
    
    print("Running JIT Speed Test (10M iterations)...")
    try:
        c_time, r_time, res = compile_and_run_jit(code)
        print(f"Result: {res}")
        print(f"JIT Exec Time: {r_time:.6f}s")
        
        # Compare with Python (approx)
        start_py = time.perf_counter()
        s, i, c = 0, 0, 10000000
        while i < c:
            s += 1
            i += 1
        py_time = time.perf_counter() - start_py
        print(f"Python Exec:   {py_time:.6f}s")
        
        print(f"Speedup: {py_time / r_time:.2f}x")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
