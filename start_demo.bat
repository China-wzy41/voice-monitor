@echo off
cd /d "%~dp0"
start "Library IoT backend" cmd /k ".venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak > nul
start "Library IoT simulator" cmd /k ".venv\Scripts\python.exe simulator.py"
start "" "http://127.0.0.1:8000/"

