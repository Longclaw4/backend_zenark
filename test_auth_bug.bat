@echo off
REM Test script for authentication bug (Windows version)
REM This script reproduces the signup → signin failure

echo.
echo ========================================
echo   Testing Authentication Bug
echo ========================================
echo.

REM Generate unique email with timestamp
set TEST_EMAIL=bugtest_%RANDOM%@example.com
set TEST_PASSWORD=TestPassword123!
set API_BASE=https://service.zenark.in/zenark

echo Test Email: %TEST_EMAIL%
echo Test Password: %TEST_PASSWORD%
echo.

REM Step 1: Signup
echo ========================================
echo Step 1: Creating new user
echo ========================================
echo.

curl -X POST "%API_BASE%/api/auth/signup" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Bug Test User\",\"email\":\"%TEST_EMAIL%\",\"password\":\"%TEST_PASSWORD%\",\"school\":\"Test School\",\"class\":\"10A\",\"roles\":[\"student\"]}"

echo.
echo.

REM Wait for database sync
echo Waiting 2 seconds for database sync...
timeout /t 2 /nobreak >nul
echo.

REM Step 2: Signin
echo ========================================
echo Step 2: Attempting signin
echo ========================================
echo.

curl -X POST "%API_BASE%/api/auth/signin" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"%TEST_EMAIL%\",\"password\":\"%TEST_PASSWORD%\"}"

echo.
echo.
echo ========================================
echo Test Complete
echo ========================================
echo.
echo If you see a 500 error above, the bug is confirmed.
echo If you see a token, the bug is fixed!
echo.

pause
