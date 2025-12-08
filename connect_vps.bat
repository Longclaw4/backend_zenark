@echo off
REM ============================================
REM VPS SSH Connection Helper for Windows
REM ============================================

echo.
echo ========================================
echo   Mental Health Bot VPS Manager
echo ========================================
echo.
echo Server: 72.61.170.25
echo Username: root
echo Password: GenericPassword123#
echo.
echo Connecting to VPS...
echo.

REM Connect to VPS
ssh root@72.61.170.25

REM If connection fails
if errorlevel 1 (
    echo.
    echo ========================================
    echo   Connection Failed!
    echo ========================================
    echo.
    echo Troubleshooting:
    echo 1. Check your internet connection
    echo 2. Verify the server is online
    echo 3. Ensure SSH is installed on Windows
    echo.
    echo To install SSH on Windows:
    echo - Open Settings ^> Apps ^> Optional Features
    echo - Add "OpenSSH Client"
    echo.
    pause
)
