# Beijing Air Quality Analytics Dashboard 🌫️

Dashboard interaktif berbasis Streamlit untuk menganalisis tren polusi udara (PM2.5), pengaruh faktor meteorologi, dan sebaran spasial kualitas udara di 12 stasiun pemantauan wilayah Beijing periode Maret 2013 – Februari 2017.

---

## Fitur Utama Dashboard

| Fitur | Deskripsi |
|-------|-----------|
| **Filter Interaktif** | Pilihan stasiun pemantauan & rentang waktu dinamis pada sidebar |
| **Metrik Utama** | Ringkasan rata-rata PM2.5, total data terverifikasi, dan indikator risiko kualitas udara |
| **Tren Temporal** | Visualisasi fluktuasi bulanan dan siklus musiman konsentrasi PM2.5 |
| **Korelasi Meteorologi** | Matriks korelasi parameter cuaca (angin, suhu, titik embun, tekanan, curah hujan) terhadap PM2.5 |
| **Klasifikasi AQI** | Distribusi frekuensi kategori kualitas udara standar US-EPA/WHO |
| **Peta Spasial Interaktif** | Sebaran 12 stasiun pemantauan dengan marker warna sesuai tingkat polusi |

---

## Struktur Direktori Proyek

```text
submission/
├── dashboard/
│   ├── main_data.csv          # Dataset bersih hasil preprocessing
│   └── dashboard.py           # Script utama dashboard Streamlit
├── data/
│   └── PRSA_Data_*.csv        # 12 file dataset mentah (12 stasiun)
├── notebook.ipynb             # Notebook analisis lengkap (Google Colab)
├── README.md                  # Dokumentasi proyek ini
├── requirements.txt           # Daftar dependensi Python
└── url.txt                    # Tautan dashboard Streamlit Cloud

---
```
## Panduan Instalasi & Menjalankan Dashboard

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```
## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
cd dashboard
streamlit run dashboard.py
```