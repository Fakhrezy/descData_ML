#!/usr/bin/env python3
"""
Script untuk memeriksa isi file model yang ada
"""

import joblib
import os

model_path = "schizophrenia_svm_model.pkl"

print("=== Checking Model File ===")
print(f"Model file path: {os.path.abspath(model_path)}")
print(f"Model file exists: {os.path.exists(model_path)}")

if os.path.exists(model_path):
    try:
        model_data = joblib.load(model_path)
        print(f"Model data type: {type(model_data)}")
        print(
            f"Model data keys: {list(model_data.keys()) if isinstance(model_data, dict) else 'Not a dict'}"
        )

        if isinstance(model_data, dict):
            for key, value in model_data.items():
                print(f"  {key}: {type(value)}")

    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print("Model file does not exist")

print("\n=== Checking models directory ===")
models_dir = "models"
if os.path.exists(models_dir):
    files = os.listdir(models_dir)
    print(f"Files in models directory: {files}")

    for file in files:
        if file.endswith(".pkl"):
            file_path = os.path.join(models_dir, file)
            print(f"\nChecking {file}:")
            try:
                data = joblib.load(file_path)
                print(f"  Type: {type(data)}")
                if isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())}")
            except Exception as e:
                print(f"  Error: {e}")
else:
    print("Models directory does not exist")
