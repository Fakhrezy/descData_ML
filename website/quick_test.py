#!/usr/bin/env python3
"""
Quick model test
"""
import joblib
import os

# Check if model file exists
model_path = "schizophrenia_svm_model.pkl"
print(f"Model file exists: {os.path.exists(model_path)}")

if os.path.exists(model_path):
    try:
        # Load model data
        model_data = joblib.load(model_path)
        print("Model loaded successfully")
        print(f"Model data keys: {list(model_data.keys())}")

        # Check if this is our expected format
        expected_keys = [
            "model",
            "scaler",
            "label_encoder",
            "feature_columns",
            "class_names",
        ]
        for key in expected_keys:
            exists = key in model_data
            print(f"  {key}: {'✓' if exists else '✗'}")

        print("\nTesting model prediction...")
        model = model_data["model"]
        scaler = model_data["scaler"]
        label_encoder = model_data["label_encoder"]
        feature_columns = model_data["feature_columns"]
        class_names = model_data["class_names"]

        print(f"Feature columns: {feature_columns}")
        print(f"Class names: {class_names}")

        # Test prediction
        import pandas as pd
        import numpy as np

        test_features = [25, 1, 2, 3.5, 2.0, 1.5, 4.0, 3.0]
        features_df = pd.DataFrame([test_features], columns=feature_columns)
        features_scaled = scaler.transform(features_df)

        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]

        predicted_class = label_encoder.inverse_transform([prediction])[0]

        print(f"Test prediction: {predicted_class}")
        print(f"Probabilities: {dict(zip(class_names, probabilities))}")

        print("\n✓ Model is working correctly!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
else:
    print("Model file not found!")
