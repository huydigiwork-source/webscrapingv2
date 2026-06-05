@echo off
echo ===== PUSH START =====

git add .

git commit -m "auto update %date% %time%"

git push origin main

echo ===== PUSH DONE =====
pause