@echo off
echo.
echo =========================================
echo    Image Encryption Tool - Installation
echo =========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo [✓] Python found
    goto check_pip
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    py --version
    echo [✓] Python found (using py launcher)
    goto check_pip
)

echo [✗] Python not found!
echo.
echo Please install Python 3.6 or higher:
echo  1. Download from https://python.org
echo  2. Run the installer
echo  3. Check "Add Python to PATH"
echo.
pause
exit /b 1

:check_pip
echo.
echo Checking pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% equ 0 (
    goto install_pillow
)

echo [✗] pip not found
echo Installing pip...
curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
del get-pip.py

:install_pillow
echo.
echo Installing Pillow library...
python -m pip install pillow --quiet

if %errorlevel% equ 0 (
    echo [✓] Pillow installed successfully
) else (
    echo [✗] Failed to install Pillow
    echo Trying alternative method...
    python -m pip install --user pillow
)

echo.
echo =========================================
echo        Installation Complete!
echo =========================================
echo.
echo To run the tool:
echo   python image_tool.py
echo   or double-click image_tool.py
echo.
echo For command-line usage:
echo   python image_tool.py --help
echo.
pause
