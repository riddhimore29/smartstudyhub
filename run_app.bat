@echo off
echo Installing dependencies...
pip install flask flask-cors requests
echo.
echo Starting SmartStudyHub...
echo Open http://127.0.0.1:5000 in your browser.
python backend/app.py
pause
