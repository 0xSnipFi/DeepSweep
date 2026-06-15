# 🛡️ DeepSweep Safety Model

**Deletion is permanent. DeepSweep removes files with `os.remove` — they do NOT go
to the Recycle Bin and cannot be undone.** Read this page before clicking delete.

## What DeepSweep deletes

Only **files** inside known junk locations (temp, cache, log, update leftovers,
recycle bin). **Folders are never removed** — the directory tree stays intact so
applications keep working and simply rebuild their caches.

## What DeepSweep protects

Every candidate path is checked by `is_safe_path()`. Any path containing these is
**skipped entirely**, even if it appears in a scan list:

```
\Windows\System32   \Windows\SysWOW64   \Windows\System    \Windows\config
\Windows\security   \Windows\servicing  \Windows\drivers   \Windows\WinSxS\
\Program Files\     \Program Files (x86)\
\Boot\              \EFI\               \Recovery\
```

This is why clearing caches will **not** corrupt Windows or cause a crash. Files
that are in use are caught by `try/except` and skipped rather than forcing an error.

## ⚠️ The "Virus Scan" is a heuristic, NOT an antivirus

The Virus Scan mode flags files purely by **filename substrings** and extension —
it does **not** inspect file contents, hashes, or signatures. Words like
`crypt`, `encrypt`, `ransom`, `spy`, `tracker`, `trojan` trigger a match.

This produces **frequent false positives** on legitimate files, for example:

| Flagged as | Reality |
|------------|---------|
| `Temp\_MEIxxxxx` | PyInstaller's own temp extraction (incl. DeepSweep itself) |
| `.android\avd\*.avd` | Your Android emulator virtual device |
| files named `*tracker*`, `*crypt*` | Normal app/data/library files |

**Do not bulk-delete Virus Scan results.** Treat them as "things to look at," not
"confirmed malware." For real malware detection use Microsoft Defender or a
reputable AV product. The System Health check is informational only and never
deletes anything.

## Recommended workflow

1. Use **START DEEP SCAN** for routine cleanup — its targets (temp/cache/log) are
   safe to delete and regenerate automatically.
2. Review the list and untick anything you are unsure about.
3. Leave **Virus Scan** results alone unless you have personally verified each file.
4. Run as Administrator only when you want the tool to reach system temp/log dirs.

## Disclaimer

DeepSweep is provided "as is" under the MIT License with **no warranty**. You are
responsible for reviewing the selected items before deleting. Back up important
data first.
