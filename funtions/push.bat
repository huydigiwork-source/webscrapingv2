@echo off
setlocal EnableDelayedExpansion

REM =========================================
REM AI DEVOPS PUSH AGENT v3
REM =========================================

REM Move from Funtions/ -> project root
cd /d "%~dp0.."

echo ========================================
echo      AI DEVOPS PUSH AGENT v3
echo ========================================
echo.

echo Current Project:
cd
echo.

REM =========================================
REM 1. CHECK GIT
REM =========================================

echo [1] Checking Git status...
git status --short

echo.

REM =========================================
REM 2. STAGE ALL
REM =========================================

echo [2] Staging changes...
git add .

if %errorlevel% neq 0 (
    echo.
    echo ERROR: git add failed
    pause
    exit /b 1
)

echo.

REM =========================================
REM 3. BUILD CHANGE REPORT
REM =========================================

echo [3] Detecting staged changes...

git diff --cached --name-status > git_diff.txt

echo ========================================
echo CHANGED FILES
echo ========================================
type git_diff.txt
echo ========================================

echo.

REM =========================================
REM 4. RISK ANALYSIS
REM =========================================

set BLOCK=0

echo [4] Risk Analysis...

findstr /I ".github/workflows/" git_diff.txt >nul
if !errorlevel! == 0 (
    echo [WARNING] Workflow modified
)

findstr /I "ci/" git_diff.txt >nul
if !errorlevel! == 0 (
    echo [WARNING] CI system modified
)

findstr /I "dashboard.py" git_diff.txt >nul
if !errorlevel! == 0 (
    echo [INFO] Dashboard modified
)

findstr /I "upload_hf.py" git_diff.txt >nul
if !errorlevel! == 0 (
    echo [WARNING] HF upload modified
)

findstr /I "deploy_space.py" git_diff.txt >nul
if !errorlevel! == 0 (
    echo [WARNING] HF deploy modified
)

echo.

REM =========================================
REM 5. CRITICAL FILE CHECK
REM =========================================

echo [5] Validating project...

if not exist ".github\workflows\autonomous.yml" (
    echo [ERROR] Missing workflow file
    set BLOCK=1
)

if not exist "dashboard.py" (
    echo [ERROR] Missing dashboard.py
    set BLOCK=1
)

if not exist "requirements.txt" (
    echo [ERROR] Missing requirements.txt
    set BLOCK=1
)

if not exist "ci\swarm_orchestrator.py" (
    echo [ERROR] Missing swarm_orchestrator.py
    set BLOCK=1
)

echo.

REM =========================================
REM 6. CHECK EMPTY COMMIT
REM =========================================

git diff --cached --quiet

if !errorlevel! == 0 (
    echo No changes detected.
    pause
    exit /b 0
)

if !BLOCK! == 1 (
    echo.
    echo ========================================
    echo PUSH BLOCKED
    echo ========================================
    pause
    exit /b 1
)

echo Project validation passed.
echo.

REM =========================================
REM 7. COMMIT
REM =========================================

echo ========================================
echo SELECT DEPLOY MODE
echo ========================================
echo.
echo 1. Dashboard Only
echo 2. Scrape Dataset Only
echo 3. Full Pipeline
echo 4. Auto AI Decision
echo.

set /p MODE=Choose option:

if "%MODE%"=="1" (
    set TAG=[dashboard]
)

if "%MODE%"=="2" (
    set TAG=[scrape]
)

if "%MODE%"=="3" (
    set TAG=[full]
)

if "%MODE%"=="4" (
    set TAG=[auto]
)

if "%TAG%"=="" (
    echo Invalid option.
    pause
    exit /b 1
)

echo.
echo Selected: %TAG%
echo.

for /f %%i in ('powershell -command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i

git commit -m "auto: swarm update !TS! %TAG%"

for /f %%i in ('powershell -command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i

git commit -m "auto: swarm update !TS!"

if %errorlevel% neq 0 (
    echo Commit failed.
    pause
    exit /b 1
)

echo.

REM =========================================
REM 8. PUSH
REM =========================================

echo [7] Pushing to GitHub...

git push origin main

if %errorlevel% neq 0 (
    echo.
    echo PUSH FAILED
    pause
    exit /b 1
)

echo.

REM =========================================
REM 9. VERIFY
REM =========================================

echo [8] Final status...
git status

echo.

echo ========================================
echo SUCCESS
echo ========================================
echo Code pushed to GitHub.
echo GitHub Actions should start automatically.
echo ========================================

pause
endlocal