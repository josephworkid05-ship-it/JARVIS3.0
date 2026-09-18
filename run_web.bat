@echo off
title J.A.R.V.I.S. Stark Industries Web HUD
cls

echo ================================================================
echo    LAUNCHING STARK INDUSTRIES J.A.R.V.I.S. HOLOGRAPHIC HUD
echo ================================================================
echo.
echo Opening browser at http://127.0.0.1:5000 ...
start http://127.0.0.1:5000

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py web/app.py
) else (
    python web/app.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo Web HUD execution halted with exit code %ERRORLEVEL%.
    pause
)
