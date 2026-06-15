#!/usr/bin/env python3
"""
Build script for DeepSweep — bundles the app into a single Windows .exe.

Run from the repo root:
    python packaging/build_exe.py

Output: dist/DeepSweep.exe
"""

import os
import subprocess
import sys

# Force UTF-8 so emoji in log lines don't crash on cp1252 consoles.
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "deepsweep", "app.py")
OUTPUT_NAME = "DeepSweep"
DIST_DIR = os.path.join(ROOT, "dist")
BUILD_DIR = os.path.join(ROOT, "build")

print("=" * 70)
print("🔨 BUILDING: DeepSweep — Windows Desktop App")
print("=" * 70)

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "-i", "NONE",
    "--collect-all", "tkinter",
    "--hidden-import=psutil",
    "--hidden-import=tkinter",
    "--distpath", DIST_DIR,
    "--workpath", BUILD_DIR,
    "--specpath", BUILD_DIR,
    "-n", OUTPUT_NAME,
    "-y",
    SCRIPT,
]

print("\n⚙️  Building optimized executable (1–2 min)...\n")
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"\n❌ Build failed: {e}")
    sys.exit(1)

exe_path = os.path.join(DIST_DIR, f"{OUTPUT_NAME}.exe")
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n✅ Build successful!\n📦 {exe_path}\n📊 Size: {size_mb:.1f} MB")
else:
    print("❌ .exe not found after build!")
    sys.exit(1)
