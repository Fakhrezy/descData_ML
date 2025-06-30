#!/bin/bash

echo "==========================================="
echo "Schizophrenia Prediction Website Setup"
echo "==========================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "[1/4] Installing required packages..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi

echo
echo "[2/4] Checking dataset..."
if [ ! -f "../dataset/SchizophreniaSymptomnsData.csv" ]; then
    echo "WARNING: Dataset not found at expected location"
    echo "Expected: ../dataset/SchizophreniaSymptomnsData.csv"
    echo "Please ensure the dataset is in the correct location"
    read -p "Press Enter to continue..."
fi

echo
echo "[3/4] Training SVM model (if needed)..."
cd models
python3 svm_model.py
cd ..

echo
echo "[4/4] Starting Flask application..."
echo
echo "Website will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo

python3 app.py
