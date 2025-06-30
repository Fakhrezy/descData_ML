import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from svm_model import SchizophreniaSVMModel
import json


def test_model():
    """Test the SVM model with sample data"""
    print("Testing Schizophrenia SVM Model...")
    print("=" * 50)

    # Initialize model
    model = SchizophreniaSVMModel()

    # Try to load existing model
    model_path = os.path.join("..", "models", "schizophrenia_svm_model.pkl")
    if model.load_model(model_path):
        print("✓ Model loaded successfully")
    else:
        print("✗ Model not found, please train the model first")
        return

    # Test cases
    test_cases = [
        {
            "name": "Test Case 1 - High Risk",
            "features": [75, 1, 1, 0.8, 0.7, 0.6, 0.5, 0.9],  # High values
            "expected": "High risk indicators",
        },
        {
            "name": "Test Case 2 - Low Risk",
            "features": [65, 0, 1, 0.1, 0.2, 0.1, 0.8, 0.2],  # Low values
            "expected": "Low risk indicators",
        },
        {
            "name": "Test Case 3 - Moderate Risk",
            "features": [70, 1, 2, 0.5, 0.4, 0.3, 0.6, 0.5],  # Moderate values
            "expected": "Moderate risk indicators",
        },
    ]

    print("\nRunning test predictions...")
    print("-" * 50)

    for i, test_case in enumerate(test_cases, 1):
        try:
            prediction, probabilities = model.predict(test_case["features"])

            print(f"\n{test_case['name']}:")
            print(f"Features: {test_case['features']}")
            print(f"Predicted Class: {prediction}")
            print(f"Expected: {test_case['expected']}")

            print("Probabilities:")
            for class_name, prob in probabilities.items():
                print(f"  {class_name}: {prob:.2f}%")

        except Exception as e:
            print(f"✗ Error in {test_case['name']}: {str(e)}")

    print("\n" + "=" * 50)
    print("Model testing completed!")


def test_api():
    """Test API endpoints"""
    try:
        import requests

        print("\nTesting API endpoints...")
        print("-" * 30)

        base_url = "http://localhost:5000"

        # Test model info endpoint
        try:
            response = requests.get(f"{base_url}/api/model-info", timeout=5)
            if response.status_code == 200:
                print("✓ Model info endpoint working")
                info = response.json()
                print(f"  Model type: {info.get('model_type', 'Unknown')}")
                print(f"  Features: {len(info.get('features', []))}")
                print(f"  Classes: {len(info.get('classes', []))}")
            else:
                print(f"✗ Model info endpoint error: {response.status_code}")
        except requests.exceptions.RequestException:
            print("✗ Cannot connect to API (server not running?)")

    except ImportError:
        print("Requests library not available, skipping API tests")


if __name__ == "__main__":
    test_model()
    test_api()
