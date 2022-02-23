#! /usr/bin/env python
__version__ = "22.0.3"

import sys
from pathlib import Path

vendor_path = Path(__file__).parent / "_vendor"
sys.path.insert(0, str(vendor_path))
