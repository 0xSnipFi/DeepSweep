# 🧹 DeepSweep

**Deep Disk Cleaner for Windows** — a fast, neon-themed desktop tool that reclaims
disk space by removing temp, cache, and log junk. Folders and system files are
protected; only safe junk files are removed.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)
![UI](https://img.shields.io/badge/ui-tkinter-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> ⚠️ **Read [docs/SAFETY.md](docs/SAFETY.md) before deleting anything.** DeepSweep
> deletes files **permanently** (no Recycle Bin). The "Virus Scan" mode is a
> filename heuristic, **not** a real antivirus — do not blindly delete its results.

---

## ✨ Features

- **Deep Scan** — walks up to 12 levels deep through known junk locations:
  - User & Windows **Temp**, Prefetch, Office `~$` leftovers
  - **Browser cache** (Chrome, Edge, Brave, Opera, Vivaldi, Firefox) incl. modern
    Chromium dirs (`Cache_Data`, `DawnCache`, `GrShaderCache`, `Network\Cache`, …)
  - **App cache** for 40+ apps (Discord, Spotify, Teams, Slack, Steam, NVIDIA,
    Adobe, JetBrains, VSCode, Cursor, …) plus a generic LocalAppData **and**
    Roaming sweep
  - **Windows cache** (thumbnails, INetCache, WebCache, font cache)
  - **Logs** (CBS, DISM, Panther, WER, crash dumps, minidumps)
  - **Windows Update** leftovers, Delivery Optimization, WinSxS temp
  - **Python** (`.pyc`/`.pyo`), **NPM/Node** caches
  - **Recycle Bin**, stray `Thumbs.db` / `.tmp` / `.dmp`
- **Selectable results** — per-item and per-category checkboxes with live size totals
- **Safe by design** — a hard path guard blocks `System32`, `WinSxS`, `Program
  Files`, `Boot`, `EFI`, `Recovery`, etc. Only **files** are deleted; folders stay.
- **Multi-drive** detection with usage bars
- **Heuristic Virus Scan** & **System Health** check (informational — see Safety)
- Neon GUI, threaded scanning, stop-anytime, no telemetry

## 🚀 Quick Start

### Run from source
```bash
git clone https://github.com/<you>/DeepSweep.git
cd DeepSweep
pip install -r requirements.txt
python -m deepsweep
```

> Tkinter ships with the standard Python installer on Windows. The only third-party
> dependency is `psutil`.

### Build a standalone .exe
```bash
pip install pyinstaller psutil
python packaging/build_exe.py
# → dist/DeepSweep.exe
```

Then double-click `dist/DeepSweep.exe`, or run `packaging/RUN_APP.bat`.
For full access (system temp/log locations), **Run as Administrator**.

## 🖱️ Usage

1. Pick the drives to scan in the left panel.
2. Click **START DEEP SCAN**.
3. Review results — untick anything you want to keep.
4. Click **DELETE SELECTED** and confirm.

## 🛡️ Safety

DeepSweep is built to be conservative, but deletion is **permanent**. The full
safety model, the list of protected paths, and why the Virus Scan results are
heuristic (and often false positives) are documented in
**[docs/SAFETY.md](docs/SAFETY.md)**. Read it.

## 📁 Project Layout

```
DeepSweep/
├── deepsweep/          # the application package
│   ├── app.py          # GUI + scan/delete engine
│   ├── __init__.py
│   └── __main__.py     # `python -m deepsweep`
├── packaging/          # build_exe.py, .bat launchers
├── tests/              # smoke tests
├── docs/               # guides + SAFETY.md
└── README.md
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs welcome — especially new
safe cache locations and bug fixes for the safety guard.

## 📜 License

[MIT](LICENSE) © 2026 Debarghya
