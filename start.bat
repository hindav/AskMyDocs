@echo off
title AskMyDocs - Dental Edition
echo Starting AskMyDocs...

:: Change to the directory of this script
cd /d %~dp0

:: Activate the conda environment
:: We use 'call conda' which assumes conda is in the PATH
call conda activate Base1

:: Run the Streamlit application
streamlit run src/app.py

:: Keep the window open if the app crashes
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Application crashed or was interrupted.
    pause
)
