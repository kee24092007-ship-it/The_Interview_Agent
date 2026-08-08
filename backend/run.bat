@echo off
REM Run the FastAPI backend in development mode.
cd /d "%~dp0"
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt
set PYTHONPATH=%cd%
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
