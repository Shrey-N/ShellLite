import sys
import os

if getattr(sys, 'frozen', False):
    # PyInstaller bundle path
    base_dir = sys._MEIPASS
else:
    # Standard Python path
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)

from src.main import main

if __name__ == "__main__":
    main()
