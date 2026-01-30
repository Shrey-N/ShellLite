
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_benchmark_graph():
    # Data from the paper
    labels = ['Interpreted Mode', 'LLVM JIT (Compiled)']
    times = [28.5, 0.001]
    
    # Colors
    colors = ['#ffaa00', '#00aa44'] # Orange, Green
    
    plt.figure(figsize=(10, 6))
    
    # Create bar chart with log scale
    bars = plt.bar(labels, times, color=colors, width=0.5)
    
    # Set log scale on Y axis
    plt.yscale('log')
    
    # Y-axis tweaks to look good with log scale
    plt.ylabel('Time (Seconds) - Log Scale', fontsize=12)
    plt.title('Runtime Performance: Interpreted vs LLVM', fontsize=14, fontweight='bold')
    
    # specific limits to make 0.001 and 28.5 look distinct
    plt.ylim(0.0001, 100) 
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.3, which='both')
    
    # Annotate bars
    for bar, time_val in zip(bars, times):
        height = bar.get_height()
        if time_val < 0.01:
            label = f"< {time_val}s"
        else:
            label = f"{time_val}s"
            
        plt.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                 label,
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Output path
    # output_file = r"c:\Users\shrey\OneDrive\Desktop\oka\benchmark_final.png"
    # Ensure it saves to the correct location as requested
    output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "benchmark_final.png")
    output_file = os.path.abspath(output_file)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Graph generated at: {output_file}")

if __name__ == "__main__":
    generate_benchmark_graph()
