@echo off
title TravelNet MRZ Reader App
color 0B

echo ====================================================
echo   TRAVELNET - Passport MRZ Bulk Reader & Renamer
echo ----------------------------------------------------
echo   Directory: %USERPROFILE%\Documents\travelnetpmrz
echo   Launching Flask server from app.py...
echo ----------------------------------------------------
echo   Visit: http://127.0.0.1:5000 in your browser
echo ====================================================

:: Go to the script directory
cd /d "%USERPROFILE%\Documents\travelnetpmrz"

:: OPTIONAL: Activate virtual environment if needed
:: call venv\Scripts\activate

:: Run the app
python app.py

pause
