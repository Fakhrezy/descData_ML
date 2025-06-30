# TUTORIAL: Menjalankan Website Prediksi Skizofrenia

## Langkah-langkah Setup dan Menjalankan Website

### 1. Persiapan Environment

1. **Pastikan Python 3.8+ terinstall**

   ```bash
   python --version
   ```

2. **Install dependencies yang diperlukan**
   ```bash
   pip install flask pandas scikit-learn numpy joblib imbalanced-learn
   ```

### 2. Struktur File yang Dibutuhkan

Pastikan struktur folder seperti ini:

```
website/
├── app.py                              # Main Flask application
├── config.py                           # Configuration file
├── requirements.txt                    # Python dependencies
├── test_system.py                      # System test script
├── models/
│   └── svm_model.py                   # SVM model training script
├── templates/
│   ├── index.html                     # Main prediction page
│   └── about.html                     # About page
├── static/
│   ├── style.css                      # Custom CSS
│   └── script.js                      # Custom JavaScript
└── ../dataset/
    └── SchizophreniaSymptomnsData.csv # Dataset file
```

### 3. Testing System

Sebelum menjalankan website, test terlebih dahulu:

```bash
cd website
python test_system.py
```

Jika test berhasil, lanjut ke langkah berikutnya.

### 4. Menjalankan Website

#### Opsi A: Manual

```bash
cd website
python app.py
```

#### Opsi B: Menggunakan Script (Windows)

```bash
cd website
run.bat
```

#### Opsi C: Menggunakan Script (Linux/Mac)

```bash
cd website
chmod +x run.sh
./run.sh
```

### 5. Mengakses Website

1. Buka browser
2. Kunjungi: `http://localhost:5000`
3. Anda akan melihat halaman prediksi

### 6. Cara Menggunakan Website

1. **Isi Form Prediksi:**

   - Age: Usia pasien (50-100 tahun)
   - Gender: Jenis kelamin (Female/Male)
   - Marital Status: Status perkawinan
   - Fatigue: Tingkat kelelahan (-1 sampai 1)
   - Slowing: Perlambatan psikomotor (-1 sampai 1)
   - Pain: Tingkat nyeri (-1 sampai 1)
   - Hygiene: Skor kebersihan diri (-1 sampai 1)
   - Movement: Kelainan gerakan (-1 sampai 1)

2. **Klik "Predict Schizophrenia Risk"**

3. **Lihat Hasil:**
   - Prediksi kelas risiko
   - Distribusi probabilitas untuk semua kelas
   - Rekomendasi berdasarkan hasil

### 7. Contoh Data Test

Gunakan tombol "Quick Test Data" untuk mengisi form dengan data sampel:

**Low Risk Sample:**

- Age: 60, Gender: Female, Marital: Married
- Fatigue: 0.1, Slowing: 0.1, Pain: 0.0
- Hygiene: 0.8, Movement: 0.2

**Moderate Risk Sample:**

- Age: 68, Gender: Female, Marital: Single
- Fatigue: 0.3, Slowing: 0.2, Pain: 0.1
- Hygiene: 0.4, Movement: 0.3

**High Risk Sample:**

- Age: 75, Gender: Male, Marital: Widowed
- Fatigue: 0.8, Slowing: 0.7, Pain: 0.6
- Hygiene: 0.2, Movement: 0.9

### 8. Fitur Website

1. **Prediksi Real-time**: Input data dan dapatkan hasil langsung
2. **Visualisasi Probabilitas**: Bar chart untuk semua kelas
3. **Copy Results**: Salin hasil ke clipboard
4. **Reset Form**: Mulai prediksi baru
5. **Sample Data**: Data test untuk demonstrasi
6. **Responsive Design**: Dapat diakses dari desktop/mobile
7. **About Page**: Informasi tentang model dan sistem

### 9. Output Kelas Prediksi

Model memprediksi 5 tingkat risiko:

- **High Proneness**: Risiko tinggi (perlu perhatian segera)
- **Elevated Proneness**: Risiko tinggi/sedang (perlu monitoring)
- **Moderate Proneness**: Risiko sedang
- **Low Proneness**: Risiko rendah
- **Minimal Proneness**: Risiko minimal

### 10. Troubleshooting

**Problem: Dataset not found**

- Pastikan file `SchizophreniaSymptomnsData.csv` ada di folder `../dataset/`
- Path relatif harus benar dari folder website

**Problem: Import error**

- Install semua dependencies: `pip install -r requirements.txt`
- Pastikan Python environment aktif

**Problem: Model training failed**

- Check dataset format dan encoding
- Pastikan tidak ada missing critical columns
- Check memory usage untuk dataset besar

**Problem: Website tidak bisa diakses**

- Pastikan Flask app running di port 5000
- Check firewall settings
- Coba akses dengan `http://127.0.0.1:5000`

### 11. Customization

**Mengubah Model Parameters:**
Edit file `models/svm_model.py`:

```python
self.model = SVC(
    kernel='rbf',          # rbf, linear, poly
    C=1.0,                 # regularization parameter
    gamma='scale',         # kernel coefficient
    probability=True,
    random_state=42
)
```

**Mengubah UI:**

- Edit `templates/index.html` untuk layout
- Edit `static/style.css` untuk styling
- Edit `static/script.js` untuk interaktivity

**Menambah Fitur:**

- Tambah endpoint baru di `app.py`
- Tambah validasi input di JavaScript
- Tambah visualisasi dengan Chart.js/Plotly

### 12. Deployment

Untuk production deployment:

1. **Set DEBUG=False** di config.py
2. **Use production WSGI server** (Gunicorn, uWSGI)
3. **Add security headers**
4. **Setup reverse proxy** (Nginx)
5. **Use HTTPS**
6. **Add logging and monitoring**

### 13. API Usage

Website juga menyediakan API endpoint:

```python
import requests

# Predict via API
data = {
    'age': 68,
    'gender': 0,
    'marital_status': 2,
    'fatigue': 0.3,
    'slowing': 0.2,
    'pain': 0.1,
    'hygiene': 0.4,
    'movement': 0.3
}

response = requests.post('http://localhost:5000/predict', data=data)
result = response.json()
print(result)
```

---

## PENTING: Disclaimer Medis

⚠️ **Peringatan**: Aplikasi ini hanya untuk tujuan edukasi dan penelitian. TIDAK boleh digunakan sebagai pengganti diagnosis medis profesional. Selalu konsultasikan dengan tenaga medis yang berkualifikasi untuk nasihat dan diagnosis medis yang akurat.
