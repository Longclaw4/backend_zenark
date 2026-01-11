@echo off
echo Checking VPS dependencies...
echo.

ssh root@72.61.170.25 "cd /root/app && echo '=== Current Directory ===' && pwd && echo. && echo '=== Python Version ===' && python3 --version && echo. && echo '=== Langchain Packages ===' && pip list | grep -i langchain && echo. && echo '=== Requirements.txt ===' && cat requirements.txt && echo. && echo '=== Service Status ===' && systemctl status fastapi --no-pager -n 20 && echo. && echo '=== Recent Logs ===' && journalctl -u fastapi -n 50 --no-pager"

pause
