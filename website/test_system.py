# Simple test script untuk menguji model
import sys
import os

# Add the models directory to the path
sys.path.append("models")


def test_basic_functionality():
    """Test basic functionality without running the full app"""
    print("=== Schizophrenia Prediction System Test ===")

    try:
        # Test imports
        import pandas as pd
        import numpy as np
        from sklearn.svm import SVC
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from imblearn.over_sampling import SMOTE
        import joblib

        print("✓ All required packages imported successfully")

        # Check dataset
        dataset_path = "../dataset/SchizophreniaSymptomnsData.csv"
        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
            print(f"✓ Dataset loaded: {len(df)} records")
            print(f"✓ Features: {list(df.columns)}")
            print(f"✓ Target classes: {df['Schizophrenia'].unique().tolist()}")
        else:
            print(f"✗ Dataset not found at: {dataset_path}")
            return False

        # Test basic preprocessing
        df_test = df.head(100).copy()  # Use small sample for testing
        df_test = df_test.fillna(df_test.mean(numeric_only=True))

        if "Name" in df_test.columns:
            df_test = df_test.drop(columns=["Name"])

        # Encode categorical variables
        le_gender = LabelEncoder()
        le_marital = LabelEncoder()
        le_target = LabelEncoder()

        df_test["Gender"] = le_gender.fit_transform(df_test["Gender"])
        df_test["Marital_Status"] = le_marital.fit_transform(df_test["Marital_Status"])
        df_test["Schizophrenia"] = le_target.fit_transform(df_test["Schizophrenia"])

        print("✓ Categorical encoding successful")

        # Test train-test split
        X = df_test.drop(columns=["Schizophrenia"])
        y = df_test["Schizophrenia"]

        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Test scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        print("✓ Data preprocessing successful")

        # Test SVM model creation
        svm_model = SVC(
            kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=42
        )
        svm_model.fit(X_train_scaled, y_train)

        # Test prediction
        predictions = svm_model.predict(X_test_scaled)
        probabilities = svm_model.predict_proba(X_test_scaled)

        print("✓ SVM model training and prediction successful")
        print(
            f"✓ Sample prediction: {le_target.inverse_transform([predictions[0]])[0]}"
        )
        print(f"✓ Sample probabilities: {probabilities[0]}")

        return True

    except Exception as e:
        print(f"✗ Error during testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def show_sample_usage():
    """Show how to use the prediction system"""
    print("\n=== Sample Usage Instructions ===")
    print("1. Run: python app.py")
    print("2. Open browser to: http://localhost:5000")
    print("3. Fill in the form with patient data:")
    print("   - Age: 68")
    print("   - Gender: Female (0) or Male (1)")
    print("   - Marital Status: 0=Divorced, 1=Married, 2=Single, 3=Widowed")
    print("   - Fatigue: 0.3 (range: -1 to 1)")
    print("   - Slowing: 0.2 (range: -1 to 1)")
    print("   - Pain: 0.1 (range: -1 to 1)")
    print("   - Hygiene: 0.4 (range: -1 to 1)")
    print("   - Movement: 0.3 (range: -1 to 1)")
    print("4. Click 'Predict Schizophrenia Risk'")
    print("5. View results with probability distribution")


if __name__ == "__main__":
    success = test_basic_functionality()
    show_sample_usage()

    if success:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nTo start the web application:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
    else:
        print("\n✗ Some tests failed. Please check the error messages above.")

    print(
        "\nNote: Make sure the dataset 'SchizophreniaSymptomnsData.csv' is in the '../dataset/' directory."
    )
