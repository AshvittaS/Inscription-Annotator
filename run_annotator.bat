@echo off
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
  python annotator_server.py
) else (
  py annotator_server.py
)
pause
