@echo off
echo Interactive Crossword Solver - Deployment
echo =========================================

echo.
echo [WORKING] Adding files to Git...
git add .

echo.
echo [WORKING] Committing changes...
git commit -m "Update interactive solver - %date% %time%"

echo.
echo [WORKING] Pushing to GitHub...
git push

echo.
echo [SUCCESS] Deployment completed!
echo Your changes are now live on Render.
echo.
pause 