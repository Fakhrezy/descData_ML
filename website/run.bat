@echo off
echo ===========================================
echo Schizophrenia Prediction Website Setup
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo [1/4] Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo [2/4] Checking dataset...
if not exist "..\dataset\SchizophreniaSymptomnsData.csv" (
    echo WARNING: Dataset not found at expected location
    echo Expected: ..\dataset\SchizophreniaSymptomnsData.csv
    echo Please ensure the dataset is in the correct location
    pause
)

echo.
echo [3/4] Training SVM model (if needed)...
cd models
python svm_model.py
cd ..

echo.
echo [4/4] Starting Flask application...
echo.
echo Website will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
