#!/usr/bin/env python3
"""
Test script untuk memeriksa apakah model SVM dapat dimuat dengan benar
"""

import os
import sys

# Add models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

try:
    from svm_model import SchizophreniaSVMModel

    print("=== Testing Model Loading ===")

    # Initialize the model
    svm_model = SchizophreniaSVMModel()

    # Check if model file exists
    model_path = "schizophrenia_svm_model.pkl"
    full_path = os.path.abspath(model_path)
    print(f"Looking for model at: {full_path}")
    print(f"Model file exists: {os.path.exists(model_path)}")

    if os.path.exists(model_path):
        # Try to load the model
        success = svm_model.load_model(model_path)
        print(f"Model loading success: {success}")

        if success:
            print(
                f"Model status: {'Loaded' if svm_model.model is not None else 'Not loaded'}"
            )
            print(
                f"Scaler status: {'Loaded' if svm_model.scaler is not None else 'Not loaded'}"
            )
            print(
                f"Label encoder status: {'Loaded' if svm_model.label_encoder is not None else 'Not loaded'}"
            )
            print(f"Features: {svm_model.feature_columns}")
            print(f"Classes: {svm_model.class_names}")

            # Test prediction
            try:
                test_features = [25, 1, 2, 3.5, 2.0, 1.5, 4.0, 3.0]  # Example data
                predicted_class, probabilities = svm_model.predict(test_features)
                print(f"\nTest prediction successful!")
                print(f"Predicted class: {predicted_class}")
                print(f"Probabilities: {probabilities}")
            except Exception as e:
                print(f"Test prediction failed: {str(e)}")
        else:
            print("Failed to load model")
    else:
        print("Model file does not exist")

        # Try to train new model
        print("\nTrying to train new model...")
        try:
            from svm_model import train_and_save_model

            accuracy = train_and_save_model()
            print(f"New model trained with accuracy: {accuracy}")

            # Try to load again
            success = svm_model.load_model(model_path)
            print(f"New model loading success: {success}")
        except Exception as e:
            print(f"Failed to train new model: {str(e)}")

except Exception as e:
    print(f"Error during testing: {str(e)}")
    import traceback

    traceback.print_exc()

print("\n=== Test Complete ===")
