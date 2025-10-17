@echo off
echo ============================================================
echo PDF Support Quick Fix for Windows
echo ============================================================
echo.

echo Step 1: Installing Python dependencies...
pip install pdf2image PyPDF2
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python packages
    pause
    exit /b 1
)
echo DONE!
echo.

echo Step 2: Checking for Poppler...
where pdftoppm >nul 2>&1
if %errorlevel% equ 0 (
    echo Poppler is already installed!
    echo.
    goto :restart
)

echo Poppler is NOT installed.
echo.
echo Please install Poppler manually:
echo 1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/
echo 2. Extract to C:\Program Files\poppler
echo 3. Add C:\Program Files\poppler\Library\bin to System PATH
echo.
echo After installing Poppler, run this script again.
echo.
pause
exit /b 1

:restart
echo ============================================================
echo All dependencies installed!
echo ============================================================
echo.
echo You can now:
echo 1. Restart your application: python app.py
echo 2. Upload PDF files
echo.
pause