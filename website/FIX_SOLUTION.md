# Solusi untuk Error "Model Not Trained Yet"

## Masalah yang Ditemukan:

Error "model not trained yet" terjadi karena:

1. **Path model salah** - Model ada di direktori root, bukan di folder models
2. **Import error** - Path import untuk svm_model tidak benar
3. **Model loading gagal** - Tidak ada error handling yang proper

## Perbaikan yang Telah Dilakukan:

### 1. Fix Path Model (app.py)

```python
# SEBELUM:
model_path = os.path.join("models", "schizophrenia_svm_model.pkl")

# SESUDAH:
model_path = "schizophrenia_svm_model.pkl"  # Model is in root directory
```

### 2. Fix Import Path (app.py)

```python
# Add models directory to path
models_path = os.path.join(os.path.dirname(__file__), "models")
sys.path.insert(0, models_path)
```

### 3. Tambahkan Error Handling

- Cek apakah model file exists
- Cek apakah model berhasil dimuat
- Test prediksi sebelum menjalankan server
- Exit dengan error jika ada masalah

### 4. Debug Information

- Menampilkan path absolut model file
- Status loading setiap komponen
- Test prediksi saat startup

## Cara Menjalankan:

### Opsi 1: Gunakan script batch (Windows)

```batch
test_website_fixed.bat
```

### Opsi 2: Manual via PowerShell/CMD

```powershell
cd "c:\@Storage\Documents\Data\00. itenas\06. smst VI\01. Machine Learning - Pa Jasman\reguler\code\website"
python app.py
```

### Opsi 3: Gunakan script startup

```python
python start_app.py
```

## Expected Output saat Startup:

```
✓ SVM model module imported successfully
✓ SVM model object created
Looking for model at: C:\...\schizophrenia_svm_model.pkl
Model file exists: True
✓ Model status: Loaded
✓ Features: ['Age', 'Gender', 'Marital_Status', 'Fatigue', 'Slowing', 'Pain', 'Hygiene', 'Movement']
✓ Classes: ['Elevated Proneness' 'High Proneness' 'Low Proneness' 'Minimal Proneness' 'Moderate Proneness']
✓ Model test prediction successful: Low Proneness
------------------------------------------------------------
🧠 Schizophrenia Prediction System Ready!
------------------------------------------------------------
```

## File yang Diperbaiki:

1. `app.py` - Main Flask application dengan error handling
2. `models/svm_model.py` - Model path untuk training
3. `start_app.py` - Standalone startup script
4. `test_website_fixed.bat` - Windows batch script

## Troubleshooting:

### Jika masih error "Import svm_model could not be resolved":

Ini adalah error linting VS Code, bukan runtime error. Website tetap akan berjalan.

### Jika model file tidak ditemukan:

Script akan otomatis training model baru menggunakan dataset di folder `../dataset/`

### Jika dataset tidak ditemukan:

Pastikan file `SchizophreniaSymptomnsData.csv` ada di folder `dataset/`

## Kesimpulan:

Error "model not trained yet" sekarang sudah diperbaiki dengan:

- ✅ Path model yang benar
- ✅ Error handling yang robust
- ✅ Auto-training jika model tidak ada
- ✅ Startup validation dan testing

Website sekarang siap digunakan untuk prediksi!
