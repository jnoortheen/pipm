#! /usr/bin/env python

import sys
from pathlib import Path

vendor_path = Path(__file__).parent / "_vendor"
sys.path.insert(0, str(vendor_path))
