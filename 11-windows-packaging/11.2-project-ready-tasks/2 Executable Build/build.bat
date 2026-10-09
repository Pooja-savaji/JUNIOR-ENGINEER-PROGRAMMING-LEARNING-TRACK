@echo off
echo Installing dependencies...
python -m pip install -r requirements.txt

echo Building executable...
python -m PyInstaller --clean --onefile --noconfirm app.py

echo Build completed.
pause
