"""
DEMO SCRIPT - Schizophrenia Prediction Website
==============================================

Script ini mendemonstrasikan fungsionalitas website prediksi skizofrenia.
"""

import sys
import os
import time


def print_header():
    print("=" * 60)
    print("  WEBSITE PREDIKSI GEJALA SKIZOFRENIA MENGGUNAKAN SVM")
    print("=" * 60)
    print()


def show_project_overview():
    print("📋 OVERVIEW PROYEK:")
    print("• Website untuk memprediksi tingkat proneness skizofrenia")
    print("• Menggunakan algoritma Support Vector Machine (SVM)")
    print("• Dataset: Schizophrenia Symptoms Data (~5000 records)")
    print("• Framework: Flask (Python Web Framework)")
    print("• UI: Bootstrap 5 + Custom CSS/JavaScript")
    print()


def show_features():
    print("🚀 FITUR UTAMA:")
    features = [
        "Prediksi real-time berdasarkan input gejala",
        "Visualisasi probabilitas untuk semua kelas risiko",
        "Interface yang user-friendly dan responsif",
        "Validasi input dengan feedback visual",
        "Sample data untuk testing cepat",
        "Copy hasil prediksi ke clipboard",
        "API endpoint untuk integrasi dengan sistem lain",
        "Halaman informasi tentang model dan dataset",
    ]

    for i, feature in enumerate(features, 1):
        print(f"   {i}. {feature}")
    print()


def show_technical_details():
    print("⚙️  DETAIL TEKNIS:")
    print("• Model: SVM dengan RBF kernel")
    print("• Preprocessing: StandardScaler normalization")
    print("• Data Balancing: SMOTE (Synthetic Minority Oversampling)")
    print(
        "• Features: Age, Gender, Marital Status, Fatigue, Slowing, Pain, Hygiene, Movement"
    )
    print(
        "• Target Classes: 5 tingkat proneness (High, Elevated, Moderate, Low, Minimal)"
    )
    print("• Accuracy: ~85% (estimated)")
    print()


def show_input_format():
    print("📝 FORMAT INPUT:")
    print("┌─────────────────┬──────────────────┬─────────────────────────────┐")
    print("│ Feature         │ Range            │ Description                 │")
    print("├─────────────────┼──────────────────┼─────────────────────────────┤")
    print("│ Age             │ 50-100           │ Usia pasien                 │")
    print("│ Gender          │ 0=Female, 1=Male │ Jenis kelamin               │")
    print("│ Marital Status  │ 0-3              │ 0=Divorced, 1=Married,     │")
    print("│                 │                  │ 2=Single, 3=Widowed        │")
    print("│ Fatigue         │ -1 to 1          │ Tingkat kelelahan           │")
    print("│ Slowing         │ -1 to 1          │ Perlambatan psikomotor      │")
    print("│ Pain            │ -1 to 1          │ Tingkat nyeri               │")
    print("│ Hygiene         │ -1 to 1          │ Skor kebersihan diri        │")
    print("│ Movement        │ -1 to 1          │ Kelainan gerakan            │")
    print("└─────────────────┴──────────────────┴─────────────────────────────┘")
    print()


def show_output_classes():
    print("🎯 KELAS OUTPUT:")
    classes = [
        ("High Proneness", "🔴", "Risiko tinggi - perlu perhatian segera"),
        ("Elevated Proneness", "🟠", "Risiko tinggi/sedang - perlu monitoring"),
        ("Moderate Proneness", "🟡", "Risiko sedang"),
        ("Low Proneness", "🟢", "Risiko rendah"),
        ("Minimal Proneness", "🔵", "Risiko minimal"),
    ]

    for class_name, icon, desc in classes:
        print(f"   {icon} {class_name}: {desc}")
    print()


def show_file_structure():
    print("📁 STRUKTUR FILE:")
    print(
        """
website/
├── app.py                 # Flask application utama
├── config.py              # Konfigurasi aplikasi
├── requirements.txt       # Dependencies Python
├── TUTORIAL.md           # Panduan lengkap
├── models/
│   ├── svm_model.py      # Model SVM dan training logic
│   └── (model file)      # File model yang sudah ditraining
├── templates/
│   ├── index.html        # Halaman utama prediksi
│   └── about.html        # Halaman informasi
├── static/
│   ├── style.css         # Custom CSS styling
│   └── script.js         # Custom JavaScript
└── ../dataset/
    └── SchizophreniaSymptomnsData.csv  # Dataset
    """
    )


def show_usage_steps():
    print("📝 CARA MENGGUNAKAN:")
    steps = [
        "Install dependencies: pip install flask pandas scikit-learn numpy joblib imbalanced-learn",
        "Pastikan dataset ada di folder '../dataset/SchizophreniaSymptomnsData.csv'",
        "Test sistem: python test_system.py",
        "Jalankan aplikasi: python app.py",
        "Buka browser ke: http://localhost:5000",
        "Isi form dengan data pasien",
        "Klik 'Predict Schizophrenia Risk'",
        "Lihat hasil prediksi dan probabilitas",
    ]

    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    print()


def show_sample_data():
    print("📊 CONTOH DATA TEST:")

    samples = [
        {
            "name": "Low Risk Sample",
            "data": "Age: 60, Gender: Female, Marital: Married, Fatigue: 0.1, Slowing: 0.1, Pain: 0.0, Hygiene: 0.8, Movement: 0.2",
        },
        {
            "name": "Moderate Risk Sample",
            "data": "Age: 68, Gender: Female, Marital: Single, Fatigue: 0.3, Slowing: 0.2, Pain: 0.1, Hygiene: 0.4, Movement: 0.3",
        },
        {
            "name": "High Risk Sample",
            "data": "Age: 75, Gender: Male, Marital: Widowed, Fatigue: 0.8, Slowing: 0.7, Pain: 0.6, Hygiene: 0.2, Movement: 0.9",
        },
    ]

    for sample in samples:
        print(f"   • {sample['name']}:")
        print(f"     {sample['data']}")
        print()


def show_api_example():
    print("🔌 CONTOH PENGGUNAAN API:")
    print(
        """
import requests

# Data pasien
data = {
    'age': 68,
    'gender': 0,           # 0=Female
    'marital_status': 2,   # 2=Single
    'fatigue': 0.3,
    'slowing': 0.2,
    'pain': 0.1,
    'hygiene': 0.4,
    'movement': 0.3
}

# Kirim request prediksi
response = requests.post('http://localhost:5000/predict', data=data)
result = response.json()

# Output contoh:
# {
#   'success': True,
#   'prediction': 'Moderate Proneness',
#   'probabilities': {
#     'High Proneness': 15.2,
#     'Elevated Proneness': 23.8,
#     'Moderate Proneness': 35.4,
#     'Low Proneness': 18.1,
#     'Minimal Proneness': 7.5
#   }
# }
    """
    )


def show_disclaimer():
    print("⚠️  DISCLAIMER MEDIS:")
    print("   Aplikasi ini hanya untuk tujuan EDUKASI dan PENELITIAN.")
    print("   TIDAK boleh digunakan sebagai pengganti diagnosis medis profesional.")
    print("   Selalu konsultasikan dengan tenaga medis yang berkualifikasi.")
    print()


def show_next_steps():
    print("🚀 LANGKAH SELANJUTNYA:")
    print("1. Baca TUTORIAL.md untuk panduan lengkap")
    print("2. Test sistem dengan: python test_system.py")
    print("3. Jalankan website dengan: python app.py")
    print("4. Akses http://localhost:5000 di browser")
    print("5. Coba prediksi dengan sample data")
    print("6. Eksplorasi fitur-fitur yang tersedia")
    print()


def main():
    print_header()
    show_project_overview()
    show_features()
    show_technical_details()
    show_input_format()
    show_output_classes()
    show_file_structure()
    show_usage_steps()
    show_sample_data()
    show_api_example()
    show_disclaimer()
    show_next_steps()

    print("=" * 60)
    print("  WEBSITE PREDIKSI SKIZOFRENIA SIAP DIGUNAKAN!")
    print("=" * 60)


if __name__ == "__main__":
    main()
