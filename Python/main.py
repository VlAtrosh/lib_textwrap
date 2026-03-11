

import sys
import os


_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
_data_dir = os.path.join(_project_root, "data")


if len(sys.argv) == 1:
    sys.argv = [sys.argv[0], "-d", _data_dir, "-w", "70"]

from cli import main

if __name__ == "__main__":
    exit(main())
