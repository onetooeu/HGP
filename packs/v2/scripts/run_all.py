"""HGP Research Pack v2 - Reproducibility runner

Usage:
  python run_all.py

Creates ./out with figures and CSVs.
All models are illustrative toy models.
"""
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'out'
OUT.mkdir(exist_ok=True)

print('Outputs directory:', OUT)

# In this pack, data/figures are already generated.
# This script is a placeholder for future expansion.
print('Nothing to run: figures + data are included in /out.')
print('You can regenerate by re-running the original notebook/script if extended.')
