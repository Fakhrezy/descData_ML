@echo off
echo ========================================
echo  Schizophrenia Prediction Website Test
echo ========================================

cd /d "c:\@Storage\Documents\Data\00. itenas\06. smst VI\01. Machine Learning - Pa Jasman\reguler\code\website"

echo.
echo Current directory: %CD%
echo.

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found
    pause
    exit /b 1
)

echo.
echo Checking model file...
if exist "schizophrenia_svm_model.pkl" (
    echo ✓ Model file found
) else (
    echo ✗ Model file not found
)

echo.
echo Starting website...
python app.py

pause
