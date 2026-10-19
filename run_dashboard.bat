@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m sahayam.dashboard
) else (
  python -m sahayam.dashboard
)
if errorlevel 1 (
  echo.
  echo Failed to start. Install Python 3.10+ and try again.
  pause
)
