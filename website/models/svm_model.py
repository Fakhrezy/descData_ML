import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import joblib
import os


class SchizophreniaSVMModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_columns = None
        self.class_names = None

    def train_model(self, data_path):
        """Train the SVM model with the schizophrenia dataset"""
        # Load and preprocess data
        df = pd.read_csv(data_path)

        # Handle missing values
        df = df.fillna(df.mean(numeric_only=True))

        # Drop unnecessary columns
        if "Name" in df.columns:
            df = df.drop(columns=["Name"])

        # Encode categorical variables
        le_gender = LabelEncoder()
        le_marital = LabelEncoder()

        df["Gender"] = le_gender.fit_transform(df["Gender"])
        df["Marital_Status"] = le_marital.fit_transform(df["Marital_Status"])

        # Encode target variable
        self.label_encoder = LabelEncoder()
        df["Schizophrenia"] = self.label_encoder.fit_transform(df["Schizophrenia"])
        self.class_names = self.label_encoder.classes_

        # Prepare features and target
        X = df.drop(columns=["Schizophrenia"])
        y = df["Schizophrenia"]
        self.feature_columns = X.columns.tolist()

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Apply SMOTE for balanced dataset
        smote = SMOTE(random_state=42)
        X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

        # Train SVM model
        self.model = SVC(
            kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=42
        )
        self.model.fit(X_train_smote, y_train_smote)

        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.class_names))

        return accuracy

    def predict(self, features):
        """Make prediction for given features"""
        if self.model is None:
            raise ValueError("Model not trained yet!")

        # Convert to DataFrame with proper column names
        features_df = pd.DataFrame([features], columns=self.feature_columns)

        # Scale features
        features_scaled = self.scaler.transform(features_df)

        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]

        # Convert prediction back to class name
        predicted_class = self.label_encoder.inverse_transform([prediction])[0]

        # Create probability dictionary
        prob_dict = {}
        for i, class_name in enumerate(self.class_names):
            prob_dict[class_name] = float(probabilities[i])

        return predicted_class, prob_dict

    def save_model(self, model_path):
        """Save the trained model"""
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "label_encoder": self.label_encoder,
            "feature_columns": self.feature_columns,
            "class_names": self.class_names,
        }
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")

    def load_model(self, model_path):
        """Load a trained model"""
        if os.path.exists(model_path):
            model_data = joblib.load(model_path)
            self.model = model_data["model"]
            self.scaler = model_data["scaler"]
            self.label_encoder = model_data["label_encoder"]
            self.feature_columns = model_data["feature_columns"]
            self.class_names = model_data["class_names"]
            print(f"Model loaded from {model_path}")
            return True
        return False


def train_and_save_model():
    """Train the model and save it"""
    # Path to your dataset
    data_path = "../dataset/SchizophreniaSymptomnsData.csv"
    model_path = "../schizophrenia_svm_model.pkl"  # Save to root directory

    # Create and train model
    svm_model = SchizophreniaSVMModel()
    accuracy = svm_model.train_model(data_path)

    # Save the model
    svm_model.save_model(model_path)

    return accuracy


if __name__ == "__main__":
    train_and_save_model()
