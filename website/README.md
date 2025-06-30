# Schizophrenia Prediction Website

Website untuk memprediksi kelas gejala skizofrenia menggunakan model Support Vector Machine (SVM).

## Fitur

- **Prediksi Real-time**: Input gejala pasien dan dapatkan prediksi tingkat proneness skizofrenia
- **Model SVM**: Menggunakan Support Vector Machine dengan RBF kernel
- **Interface Modern**: UI yang responsif dan user-friendly
- **Visualisasi Hasil**: Menampilkan probabilitas untuk setiap kelas prediksi
- **Data Balancing**: Menggunakan SMOTE untuk mengatasi imbalanced dataset

## Struktur Proyek

```
website/
├── app.py                 # Aplikasi Flask utama
├── requirements.txt       # Dependencies Python
├── models/
│   ├── svm_model.py      # Model SVM dan training logic
│   └── schizophrenia_svm_model.pkl  # Model yang sudah ditraining
├── templates/
│   ├── index.html        # Halaman utama prediksi
│   └── about.html        # Halaman tentang proyek
└── static/               # File CSS/JS tambahan (opsional)
```

## Instalasi

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Training Model** (Otomatis jika model belum ada)

   ```bash
   cd models
   python svm_model.py
   ```

3. **Menjalankan Website**

   ```bash
   python app.py
   ```

4. **Akses Website**
   Buka browser dan kunjungi: `http://localhost:5000`

## Input Features

Website ini menerima input berikut:

1. **Age**: Usia pasien (50-100 tahun)
2. **Gender**: Jenis kelamin (Female=0, Male=1)
3. **Marital Status**: Status perkawinan (Divorced=0, Married=1, Single=2, Widowed=3)
4. **Fatigue**: Tingkat kelelahan (-1 sampai 1)
5. **Slowing**: Perlambatan psikomotor (-1 sampai 1)
6. **Pain**: Tingkat nyeri (-1 sampai 1)
7. **Hygiene**: Skor kebersihan diri (-1 sampai 1)
8. **Movement**: Kelainan gerakan (-1 sampai 1)

## Output Classes

Model memprediksi 5 tingkat proneness skizofrenia:

- **High Proneness**: Risiko tinggi
- **Elevated Proneness**: Risiko tinggi/sedang
- **Moderate Proneness**: Risiko sedang
- **Low Proneness**: Risiko rendah
- **Minimal Proneness**: Risiko minimal

## Teknologi yang Digunakan

- **Backend**: Flask, Python
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Data Balancing**: imbalanced-learn (SMOTE)
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Model Persistence**: Joblib

## Model Details

- **Algorithm**: Support Vector Machine (SVM)
- **Kernel**: RBF (Radial Basis Function)
- **Preprocessing**: StandardScaler
- **Data Balancing**: SMOTE
- **Train-Test Split**: 80-20
- **Cross-validation**: Stratified split

## API Endpoints

- `GET /`: Halaman utama prediksi
- `POST /predict`: Endpoint untuk prediksi
- `GET /about`: Halaman informasi proyek
- `GET /api/model-info`: Informasi model (JSON)

## Contoh Request API

```python
import requests

data = {
    'age': 65,
    'gender': 1,  # Male
    'marital_status': 1,  # Married
    'fatigue': 0.5,
    'slowing': 0.3,
    'pain': 0.2,
    'hygiene': 0.4,
    'movement': 0.6
}

response = requests.post('http://localhost:5000/predict', data=data)
result = response.json()
print(result)
```

## Disclaimer

⚠️ **Peringatan Medis**: Aplikasi ini hanya untuk tujuan edukasi dan penelitian. TIDAK boleh digunakan sebagai pengganti diagnosis medis profesional. Selalu konsultasikan dengan tenaga medis yang berkualifikasi untuk nasihat dan diagnosis medis.

## Development

Untuk pengembangan lebih lanjut:

1. Tambahkan validasi input yang lebih ketat
2. Implementasi logging untuk monitoring
3. Tambahkan unit tests
4. Optimasi model dengan hyperparameter tuning
5. Tambahkan feature importance visualization
6. Implementasi authentication untuk deployment production

## License

Project ini dibuat untuk keperluan akademik dan penelitian.
