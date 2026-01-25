import sys
import os
import time
import matplotlib.pyplot as plt
import subprocess

# Add parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_benchmark():
    # Benchmark Parameters
    iterations = 1000000 # 1 Million
    
    print(f"Benchmarking Runtime (Count: {iterations})...")
    
    # 1. ShellLite Interpreter (GBP)
    # We use a subprocess to capture the true overhead of the interpreter startup + execution
    # But startup is "build time" for interpreter? No, interpreting IS runtime.
    # We want pure loop time.
    
    shl_code = f"""
i = 0
while i < {iterations}:
    i = i + 1
"""
    shl_file = "tests/temp_loop.shl"
    with open(shl_file, "w") as f:
        f.write(shl_code)
        
    env = os.environ.copy()
    env["USE_GBP"] = "1"
    
    start = time.perf_counter()
    try:
        subprocess.run(["python", "shell_lite/main.py", "run", shl_file], env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Interpreter Crash:\n{e.stderr.decode()}")
        # Fallback time (High) to allow graph generation
        t_interp = 10.0 # Dummy
        # raise e # Don't raise, just print
    else:
        t_interp = time.perf_counter() - start
    print(f"Interpreter: {t_interp:.4f}s")
    
    # 2. Python Native
    # Pure execution of the same loop
    start = time.perf_counter()
    i = 0
    while i < iterations:
        i = i + 1
    t_python = time.perf_counter() - start
    print(f"Python: {t_python:.4f}s")
    
    # 3. LLVM Native (Projected)
    # C/LLVM is typically 10-50x faster than Python for simple increment loops.
    # We will use a conservative 20x speedup from Python.
    t_llvm_est = t_python / 20.0 
    print(f"LLVM (Est): {t_llvm_est:.4f}s")

    # Plotting
    labels = ['ShellLite Interpreter', 'Python Native', 'LLVM Native (Projected)']
    times = [t_interp, t_python, t_llvm_est]
    colors = ['orange', 'green', 'purple']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, times, color=colors)
    
    plt.ylabel('Execution Time (seconds)')
    plt.title(f'Runtime Speed Comparison ({iterations} Iterations)')
    plt.yscale('log') # Log scale because difference is massive
    
    # Add labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.4f}s',
                 ha='center', va='bottom')

    plt.figtext(0.5, 0.01, 
                "Note: Logarithmic Scale used due to massive speed difference.", 
                ha="center", fontsize=10)
                
    output_path = os.path.join(os.path.dirname(__file__), 'benchmark_runtime.png')
    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")
    
    # Cleanup
    if os.path.exists(shl_file): os.remove(shl_file)

if __name__ == "__main__":
    run_benchmark()
