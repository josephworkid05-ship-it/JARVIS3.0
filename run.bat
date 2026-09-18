@echo off
title J.A.R.V.I.S. Personal AI Assistant
cls

:: Check if py launcher exists, otherwise python
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py main.py
) else (
    python main.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo System execution halted with exit code %ERRORLEVEL%.
    pause
)
