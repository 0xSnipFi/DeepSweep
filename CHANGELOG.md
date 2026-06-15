# Changelog

All notable changes to DeepSweep are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [2.0.0] — 2026-06-15

### Added
- Deep scan depth raised from 2 → 12 levels so reported sizes match what
  deletion actually removes.
- Modern Chromium browser cache subdirs (`Cache_Data`, `DawnCache`,
  `GrShaderCache`, `Network\Cache`, `blob_storage`, `File System`).
- 22+ new app cache targets (Steam, Battle.net, NVIDIA GL/DX, DirectX shader
  cache, Adobe, OneDrive, WhatsApp, Signal, Postman, Figma, Notion, JetBrains,
  Unity, Cursor, VSCode-Code variants).
- Generic Roaming (`%APPDATA%`) cache sweep in addition to LocalAppData.
- Extra log/dump targets: minidumps, `MEMORY.DMP`, performance logs.
- Extra update targets: Delivery Optimization, Network Downloader cache.
- Misc-junk now matches `.tmp`, `.dmp`, `.stackdump`, `.chk`, `Thumbs.db`.
- `docs/SAFETY.md` documenting the safety model and Virus Scan caveats.

### Changed
- Delete button pinned to the bottom of the sidebar so it stays visible on
  short screens; reduced minimum window size.
- Repackaged as the `deepsweep` Python package (`python -m deepsweep`).
- Build script forces UTF-8 output and targets the new package layout.

### Notes
- Virus Scan remains a filename heuristic, not a real antivirus. See SAFETY.md.
