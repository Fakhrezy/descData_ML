#!/usr/bin/env python3
"""
Simple startup script for the website
"""
import os
import sys

print("=== Starting Schizophrenia Prediction Website ===")
print(f"Working directory: {os.getcwd()}")

# Add models directory to path
models_path = os.path.join(os.path.dirname(__file__), "models")
sys.path.insert(0, models_path)

try:
    from svm_model import SchizophreniaSVMModel

    print("✓ SVM model module imported successfully")

    # Initialize the model
    svm_model = SchizophreniaSVMModel()
    print("✓ SVM model object created")

    # Load the trained model
    model_path = "schizophrenia_svm_model.pkl"
    print(f"Looking for model at: {os.path.abspath(model_path)}")
    print(f"Model file exists: {os.path.exists(model_path)}")

    if not svm_model.load_model(model_path):
        print("Model not found. Training new model...")
        from svm_model import train_and_save_model

        train_and_save_model()
        if not svm_model.load_model(model_path):
            print("ERROR: Failed to load model even after training!")
            sys.exit(1)

    print(
        f"✓ Model status: {'Loaded' if svm_model.model is not None else 'Not loaded'}"
    )
    print(f"✓ Features: {svm_model.feature_columns}")
    print(f"✓ Classes: {svm_model.class_names}")

    # Test prediction
    test_features = [25, 1, 2, 3.5, 2.0, 1.5, 4.0, 3.0]
    try:
        predicted_class, probabilities = svm_model.predict(test_features)
        print(f"✓ Test prediction successful: {predicted_class}")
    except Exception as e:
        print(f"✗ Test prediction failed: {e}")
        sys.exit(1)

    print("-" * 50)
    print("Starting Flask application...")

    # Now start Flask
    from flask import Flask, render_template, request, jsonify

    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/predict", methods=["POST"])
    def predict():
        try:
            # Check if model is loaded
            if svm_model.model is None:
                return jsonify({"success": False, "error": "Model not loaded properly"})

            # Get form data
            age = float(request.form["age"])
            gender = int(request.form["gender"])
            marital_status = int(request.form["marital_status"])
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
            probabilities_percent = {
                k: round(v * 100, 2) for k, v in probabilities.items()
            }

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
        return render_template("about.html")

    @app.route("/api/model-info")
    def model_info():
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

    # Start the app
    print("✓ Flask app started successfully!")
    print("🌐 Website available at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host="0.0.0.0", port=5000)

except Exception as e:
    print(f"✗ Error during startup: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
