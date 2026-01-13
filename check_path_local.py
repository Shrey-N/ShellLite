
import sys
import os
print(f"CWD: {os.getcwd()}")
print(f"sys.path: {sys.path}")
try:
    import shell_lite.interpreter
    print(f"shell_lite location: {os.path.dirname(shell_lite.__file__)}")
    print(f"interpreter file: {shell_lite.interpreter.__file__}")
except ImportError as e:
    print(f"ImportError: {e}")
