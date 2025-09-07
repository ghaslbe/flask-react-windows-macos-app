@echo off
echo Building User Management Application...

echo.
echo Step 1: Installing Python requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Python requirements
    pause
    exit /b 1
)

echo.
echo Step 2: Building executable...
python build_exe.py
if %errorlevel% neq 0 (
    echo Error building executable
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo The executable is located at: dist\Benutzerverwaltung.exe
echo.
echo You can now run the application by double-clicking the executable.
echo The application will automatically open in your web browser.
echo.
pause