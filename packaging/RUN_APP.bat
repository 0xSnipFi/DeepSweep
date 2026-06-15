@echo off
REM DeepSweep launcher. Prefers the built exe, falls back to running from source.
cd /d "%~dp0\.."

if exist "dist\DeepSweep.exe" (
    start "" "dist\DeepSweep.exe"
) else (
    echo Built exe not found, running from source...
    python -m deepsweep
)
