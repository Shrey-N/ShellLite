import subprocess
import sys

cmd = [sys.executable, '-m', 'src.main', 'examples/test_phase2.sh']
print(f"Running: {cmd}")
try:
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=r'c:\Users\shrey\OneDrive\Desktop\oka')
    print("STDOUT:\n", res.stdout)
    print("STDERR:\n", res.stderr)
except Exception as e:
    print("EXCEPTION:", e)
