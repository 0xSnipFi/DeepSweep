<div align="center">

<img src="https://img.shields.io/badge/Deep-Sweep-00ff88?style=for-the-badge&labelColor=0a0a0a&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMwMGZmODgiIHN0cm9rZS13aWR0aD0iMiI+PHBhdGggZD0iTTMgNmgxOE0xNiA2VjRhMiAyIDAgMCAwLTItMmgtNGEyIDIgMCAwIDAtMiAydjJNMTkgNnYxNGEyIDIgMCAwIDEtMiAySDdhMiAyIDAgMCAxLTItMlY2Ii8+PC9zdmc+" alt="DeepSweep" />

<br/>

# DeepSweep

**Fast, safe disk cleaner for Windows**

Reclaim gigabytes of wasted space by removing temp files, browser cache, app junk, and system logs — with a neon-themed GUI that makes cleanup satisfying.

<br/>

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://github.com/0xSnipFi/DeepSweep)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/github/v/release/0xSnipFi/DeepSweep?style=flat-square&color=00ff88&label=latest)](https://github.com/0xSnipFi/DeepSweep/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/0xSnipFi/DeepSweep/total?style=flat-square&color=blueviolet&label=downloads)](https://github.com/0xSnipFi/DeepSweep/releases)

<br/>

[**Download .exe**](https://github.com/0xSnipFi/DeepSweep/releases/latest) | [Safety Guide](docs/SAFETY.md) | [Contributing](CONTRIBUTING.md) | [Changelog](CHANGELOG.md)

</div>

---

> **Warning** — DeepSweep deletes files **permanently** (no Recycle Bin). Read [docs/SAFETY.md](docs/SAFETY.md) before deleting anything. The "Virus Scan" is a filename heuristic, **not** a real antivirus.

## Download & Run

**[Download `DeepSweep.exe` from the latest release](https://github.com/0xSnipFi/DeepSweep/releases/latest)** — no Python, no install, just double-click.

For full access to system temp/log locations, right-click the exe and select **Run as administrator**.

> Windows SmartScreen may warn on first run (the exe is unsigned). Click **More info** then **Run anyway**.

## Features

| Category | What gets cleaned |
|----------|-------------------|
| **System temp** | User & Windows Temp, Prefetch, Office `~$` leftovers |
| **Browser cache** | Chrome, Edge, Brave, Opera, Vivaldi, Firefox — incl. `Cache_Data`, `DawnCache`, `GrShaderCache`, `Network\Cache` |
| **App cache** | Discord, Spotify, Teams, Slack, Steam, NVIDIA, Adobe, JetBrains, VSCode, Cursor + 30 more |
| **Windows cache** | Thumbnails, INetCache, WebCache, font cache |
| **Logs & dumps** | CBS, DISM, Panther, WER, crash dumps, minidumps |
| **Update junk** | Windows Update leftovers, Delivery Optimization, WinSxS temp |
| **Dev caches** | Python `.pyc`/`.pyo`, NPM/Node caches |
| **Misc** | Recycle Bin, `Thumbs.db`, `.tmp`, `.dmp` files |

### Highlights

- **12-level deep scan** across all connected drives
- **Per-item checkboxes** with live size totals — review before deleting
- **Hard path guard** — `System32`, `WinSxS`, `Program Files`, `Boot`, `EFI`, `Recovery` are always protected
- **Multi-drive detection** with visual usage bars
- **Heuristic virus scan** and **system health check** (informational only)
- **Threaded scanning** with stop-anytime support
- **Zero telemetry** — nothing leaves your machine

## Quick Start

### From source

```bash
git clone https://github.com/0xSnipFi/DeepSweep.git
cd DeepSweep
pip install -r requirements.txt
python -m deepsweep
```

> Tkinter ships with the standard Python installer. The only external dependency is `psutil`.

### Build standalone .exe

```bash
pip install pyinstaller psutil
python packaging/build_exe.py
# output: dist/DeepSweep.exe
```

## How to Use

```
1. Launch DeepSweep
2. Select drives to scan in the left panel
3. Click  START DEEP SCAN
4. Review results — untick anything you want to keep
5. Click  DELETE SELECTED  and confirm
```

## Safety

DeepSweep is conservative by design, but deletion is **permanent**. The full safety model, protected path list, and why virus scan results are heuristic (often false positives) are documented in **[docs/SAFETY.md](docs/SAFETY.md)**.

## Project Structure

```
DeepSweep/
├── deepsweep/           # Application package
│   ├── app.py           # GUI + scan/delete engine
│   ├── __init__.py      # Version + entry
│   └── __main__.py      # python -m deepsweep
├── packaging/           # build_exe.py, .bat launchers
├── docs/                # Safety guide
├── .github/workflows/   # CI build + release automation
└── tests/               # Smoke tests
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs welcome — especially new safe cache locations and bug fixes for the safety guard.

## License

[MIT](LICENSE) &copy; 2026 Debarghya

---

<div align="center">
<sub>Built with Python + Tkinter. No bloat, no telemetry, no cloud.</sub>
</div>
