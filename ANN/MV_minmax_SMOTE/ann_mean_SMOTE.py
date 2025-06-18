import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from imblearn.over_sampling import SMOTE  # Tambahkan ini
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Load dataset
df = pd.read_csv('schizo_symptons.csv')

# 2. Hapus kolom 'Name' jika ada
if 'Name' in df.columns:
    df.drop(columns=['Name'], inplace=True)

# 3. Label Encoding untuk fitur kategorikal
le_gender = LabelEncoder()
le_marital = LabelEncoder()
le_target = LabelEncoder()

df['Gender'] = le_gender.fit_transform(df['Gender'])
df['Marital_Status'] = le_marital.fit_transform(df['Marital_Status'])
df['Schizophrenia'] = le_target.fit_transform(df['Schizophrenia'])

# Cetak mapping label target
print("Mapping Label Schizophrenia:")
print(dict(zip(le_target.classes_, le_target.transform(le_target.classes_))))

# 4. Isi nilai kosong dengan rata-rata kolom 
df.fillna(df.mean())

# 5. Normalisasi fitur 'Age' menggunakan Min-Max Scaling
scaler = MinMaxScaler()
df['Age'] = scaler.fit_transform(df[['Age']])

# 6. Pisahkan fitur dan label
X = df.drop(columns=['Schizophrenia'])
y = df['Schizophrenia']

# 7. Bagi data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 8. Terapkan SMOTE pada data latih
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# 9. Bangun model FFNN multi-kelas
model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(5, activation='softmax'))  # 5 kelas output

# 10. Compile model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 11. Latih model
history = model.fit(X_train_smote, y_train_smote,
                    epochs=100,
                    batch_size=10,
                    validation_data=(X_test, y_test))

# 12. Evaluasi model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\nAkurasi Model pada Data Test: {accuracy:.4f}")

# 13. Prediksi dan evaluasi
y_pred_probs = model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)

# 14. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le_target.classes_)
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - Schizophrenia Proneness")
plt.show()

# 15. Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le_target.classes_))
