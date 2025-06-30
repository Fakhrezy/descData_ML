# Flask Configuration
DEBUG = True
HOST = "0.0.0.0"
PORT = 5000

# Model Configuration
MODEL_PATH = "models/schizophrenia_svm_model.pkl"
DATASET_PATH = "../dataset/SchizophreniaSymptomnsData.csv"

# Feature Configuration
FEATURE_RANGES = {
    "age": {"min": 50, "max": 100},
    "gender": {"min": 0, "max": 1},  # 0=Female, 1=Male
    "marital_status": {
        "min": 0,
        "max": 3,
    },  # 0=Divorced, 1=Married, 2=Single, 3=Widowed
    "fatigue": {"min": -1, "max": 1},
    "slowing": {"min": -1, "max": 1},
    "pain": {"min": -1, "max": 1},
    "hygiene": {"min": -1, "max": 1},
    "movement": {"min": -1, "max": 1},
}

# UI Configuration
APP_TITLE = "Schizophrenia Symptom Prediction"
APP_DESCRIPTION = "Prediksi tingkat proneness skizofrenia menggunakan model SVM"
