@echo off
REM Create a Desktop shortcut for DeepSweep (points at the built exe).
setlocal enabledelayedexpansion

set "ROOT=%~dp0.."
set "APP_PATH=%ROOT%\dist\DeepSweep.exe"
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_PATH=%DESKTOP%\DeepSweep.lnk"

if not exist "%APP_PATH%" (
    echo ERROR: App not found at: %APP_PATH%
    echo Please run: python packaging\build_exe.py
    pause
    exit /b 1
)

powershell -NoProfile -Command ^
  "$W = New-Object -ComObject WScript.Shell; " ^
  "$S = $W.CreateShortcut('%SHORTCUT_PATH%'); " ^
  "$S.TargetPath = '%APP_PATH%'; " ^
  "$S.WorkingDirectory = '%ROOT%'; " ^
  "$S.Description = 'DeepSweep - Deep Disk Cleaner'; " ^
  "$S.IconLocation = '%APP_PATH%'; " ^
  "$S.Save()"

if exist "%SHORTCUT_PATH%" (
    echo Shortcut created: %SHORTCUT_PATH%
) else (
    echo ERROR: Failed to create shortcut
)
pause
