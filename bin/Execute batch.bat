@echo off
REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Python is not installed or not in PATH.
  echo Download Python from https://python.org
  pause
  exit
)

REM Run the Python script in the same folder as the BAT file
python "%~dp0Mask_Batch.py"
pause