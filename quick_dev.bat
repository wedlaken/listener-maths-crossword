@echo off
echo Interactive Crossword Solver - Quick Development
echo ================================================

echo.
echo [WORKING] Generating HTML from interactive_solver.py...
python interactive_solver.py

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to generate HTML
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Quick development completed!
echo.
echo Summary:
echo    [SUCCESS] HTML generated from interactive_solver.py
echo    [SUCCESS] Static file saved to static/interactive_solver.html
echo    [SUCCESS] Ready for Flask app testing
echo.
echo To test locally: python app.py
echo To deploy: git add . && git commit -m "Update" && git push
echo.
pause 