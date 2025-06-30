from flask import Flask, render_template, request, jsonify
import os
import sys

# Add models directory to path
models_path = os.path.join(os.path.dirname(__file__), "models")
sys.path.insert(0, models_path)

try:
    from svm_model import SchizophreniaSVMModel

    print("✓ SVM model module imported successfully")
except ImportError as e:
    print(f"✗ Failed to import SVM model: {e}")
    sys.exit(1)

app = Flask(__name__)

# Initialize the model
try:
    svm_model = SchizophreniaSVMModel()
    print("✓ SVM model object created")
except Exception as e:
    print(f"✗ Failed to create SVM model object: {e}")
    sys.exit(1)

# Load the trained model
model_path = "schizophrenia_svm_model.pkl"  # Model is in root directory
print(f"Looking for model at: {os.path.abspath(model_path)}")
print(f"Model file exists: {os.path.exists(model_path)}")

try:
    if not svm_model.load_model(model_path):
        print("Model not found. Training new model...")
        # If model doesn't exist, train it
        try:
            from svm_model import train_and_save_model

            print("Training new model...")
            train_and_save_model()
            print("Model training completed")
        except Exception as e:
            print(f"✗ Failed to train model: {e}")
            sys.exit(1)

        if not svm_model.load_model(model_path):
            print("ERROR: Failed to load model even after training!")
            sys.exit(1)

    print(
        f"✓ Model status: {'Loaded' if svm_model.model is not None else 'Not loaded'}"
    )
    print(f"✓ Features: {svm_model.feature_columns}")
    print(f"✓ Classes: {svm_model.class_names}")

    # Test model prediction to ensure it's working
    test_features = [75, 1, 2, 0.5, 0.3, 0.2, 0.8, 0.4]  # Example values
    try:
        test_pred, test_prob = svm_model.predict(test_features)
        print(f"✓ Model test prediction successful: {test_pred}")
    except Exception as e:
        print(f"✗ Model test prediction failed: {e}")
        sys.exit(1)

except Exception as e:
    print(f"✗ Error during model loading: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("-" * 60)
print("🧠 Schizophrenia Prediction System Ready!")
print("-" * 60)


@app.route("/")
def index():
    """Main page with prediction form"""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Handle prediction requests"""
    try:
        # Check if model is loaded
        if svm_model.model is None:
            return jsonify({"success": False, "error": "Model not loaded properly"})

        # Get form data
        age = float(request.form["age"])
        gender = int(request.form["gender"])  # 0=Female, 1=Male
        marital_status = int(
            request.form["marital_status"]
        )  # 0=Divorced, 1=Married, 2=Single, 3=Widowed
        fatigue = float(request.form["fatigue"])
        slowing = float(request.form["slowing"])
        pain = float(request.form["pain"])
        hygiene = float(request.form["hygiene"])
        movement = float(request.form["movement"])

        # Prepare features
        features = [
            age,
            gender,
            marital_status,
            fatigue,
            slowing,
            pain,
            hygiene,
            movement,
        ]

        print(f"Predicting for features: {features}")

        # Make prediction
        predicted_class, probabilities = svm_model.predict(features)

        # Convert to percentage
        probabilities_percent = {k: round(v * 100, 2) for k, v in probabilities.items()}

        return jsonify(
            {
                "success": True,
                "prediction": predicted_class,
                "probabilities": probabilities_percent,
            }
        )

    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})


@app.route("/about")
def about():
    """About page with model information"""
    return render_template("about.html")


@app.route("/api/model-info")
def model_info():
    """API endpoint to get model information"""
    return jsonify(
        {
            "model_type": "Support Vector Machine (SVM)",
            "kernel": "RBF",
            "features": svm_model.feature_columns,
            "classes": (
                svm_model.class_names.tolist()
                if svm_model.class_names is not None
                else []
            ),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
