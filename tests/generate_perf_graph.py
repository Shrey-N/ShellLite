import sys
import os
import time
import matplotlib.pyplot as plt

# Add parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shell_lite.lexer import Lexer
from shell_lite.parser import Parser
from shell_lite.parser_gbp import GeometricBindingParser

HAS_LLVM = False
try:
    from shell_lite.llvm_backend.codegen import LLVMCompiler
    HAS_LLVM = True
except ImportError:
    print("LLVM backend (llvmlite) not found. Skipping LLVM benchmark.")

def generate_large_file(lines=1000):
    code = "x = 0\n"
    for i in range(lines):
        code += f"if x < {i}:\n"
        code += f"    x = x + 1\n"
    return code

def run_benchmark():
    sizes = [1000, 5000, 10000, 20000, 50000]
    
    times_old = []
    times_gbp = []
    times_py = []
    times_llvm = []
    
    for size in sizes:
        print(f"Benchmarking size: {size} lines...")
        source_shl = generate_large_file(size)
        source_py = source_shl.replace("x = x + 1", "x += 1")

        # Lexing once for consistent token comparison (though GBP might be faster if we included lexing, let's include lexing for realism)
        # Actually GBP relies on Lexer. The Old Parser relies on Lexer.
        # So we should benchmark "Lex + Parse" for true measure.
        
        # 1. Old Parser (Lex + Parse)
        start = time.perf_counter()
        l = Lexer(source_shl)
        toks = l.tokenize()
        Parser(toks).parse()
        times_old.append(time.perf_counter() - start)
        
        # 2. GBP Parser (Lex + Scan + Bind)
        start = time.perf_counter()
        l = Lexer(source_shl)
        toks = l.tokenize()
        GeometricBindingParser(toks).parse()
        times_gbp.append(time.perf_counter() - start)
        
        # 3. Python Native (Compile)
        start = time.perf_counter()
        compile(source_py, '<string>', 'exec')
        times_py.append(time.perf_counter() - start)
        
        # 4. LLVM (Lex + GBP Parse + Codegen)
        # We assume we want to use the FASTER parser for LLVM codegen to show best-case compilation.
        start = time.perf_counter()
        if HAS_LLVM:
            l = Lexer(source_shl)
            toks = l.tokenize()
            # Use GBP for speed
            ast = GeometricBindingParser(toks).parse()
            LLVMCompiler().compile(ast)
            times_llvm.append(time.perf_counter() - start)
        else:
            times_llvm.append(0)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_old, label='Old Parser', marker='o', color='red')
    plt.plot(sizes, times_gbp, label='GBP Parser', marker='s', color='blue')
    plt.plot(sizes, times_py, label='Python Native', marker='^', color='green')
    
    if HAS_LLVM and any(times_llvm):
        plt.plot(sizes, times_llvm, label='LLVM Compile (via GBP)', marker='x', color='purple', linestyle='--')

    plt.xlabel('Lines of Code')
    plt.ylabel('Time (seconds)')
    plt.title('Parsing/Compilation Speed vs Code Size')
    plt.legend()
    plt.grid(True)
    
    output_path = os.path.join(os.path.dirname(__file__), 'benchmark_scaling.png')
    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    run_benchmark()
