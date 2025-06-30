import sys
import os

sys.path.append("models")

from models.svm_model import SchizophreniaSVMModel

# Test model loading
svm_model = SchizophreniaSVMModel()
model_path = "schizophrenia_svm_model.pkl"

print("Model exists:", os.path.exists(model_path))
success = svm_model.load_model(model_path)
print("Load success:", success)

if success:
    print("Model is loaded:", svm_model.model is not None)
    print("Scaler is loaded:", svm_model.scaler is not None)
    print("Feature columns:", svm_model.feature_columns)
    print("Class names:", svm_model.class_names)

    # Test prediction
    test_features = [25, 1, 2, 3.5, 2.0, 1.5, 4.0, 3.0]
    try:
        pred, prob = svm_model.predict(test_features)
        print("Prediction:", pred)
        print("Probabilities:", prob)
    except Exception as e:
        print("Prediction error:", e)
