@echo off
cd /d "%~dp0"
set PORT=8686
where py >nul 2>nul
if %errorlevel%==0 (
  start "" http://localhost:%PORT%/index.html
  py "%~dp0serve.py" %PORT%
  goto :eof
)
where python >nul 2>nul
if %errorlevel%==0 (
  start "" http://localhost:%PORT%/index.html
  python "%~dp0serve.py" %PORT%
  goto :eof
)
echo Python not found. Please install Python 3 first.
pause
