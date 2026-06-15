"""
DeepSweep — Deep Disk Cleaner for Windows.

A fast, safe, neon-themed GUI tool that reclaims disk space by removing
temp / cache / log junk. System files are protected by a hard path guard.
"""

from .app import main

__version__ = "2.0.0"
__all__ = ["main"]
