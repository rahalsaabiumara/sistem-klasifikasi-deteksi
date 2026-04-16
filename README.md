# EduDetect

**EduDetect** adalah aplikasi berbasis web yang menggunakan kecerdasan buatan untuk mendeteksi tingkat perhatian siswa selama pembelajaran online. Sistem ini membantu guru memantau keterlibatan siswa secara real-time dan mendapatkan analisis mendalam untuk meningkatkan efektivitas pengajaran.

## Fitur Utama

- **Deteksi Wajah Real-time**: Menggunakan model YOLO untuk mendeteksi wajah siswa dalam video.
- **Klasifikasi Perhatian**: Mengklasifikasikan siswa sebagai "memperhatikan" atau "tidak memperhatikan" berdasarkan analisis visual.
- **Analisis Video**: Menganalisis video yang diunggah untuk menghasilkan laporan komprehensif.
- **Summary AI**: Menggunakan Gemini API untuk memberikan evaluasi pembelajaran dan saran konkret bagi guru.
- **Dashboard Interaktif**: Visualisasi data yang mudah dipahami dengan grafik dan statistik real-time.

## Instalasi

1. **Clone repository** (jika belum):
   ```bash
   git clone <url-repository>
   cd sistem-klasifikasi-deteksi
   ```

2. **Buat virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Aktifkan virtual environment**:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Instal dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Konfigurasi API Key**:
   Buat file `.env` di root directory dengan format berikut:
   ```env
   GEMINI_API_KEY=masukkan_gemini_api_key_anda
   ```

## Menjalankan Aplikasi

Setelah instalasi selesai, jalankan aplikasi dengan perintah:

```bash
streamlit run edudetect.py
```

Buka browser dan akses `http://localhost:8501` untuk menggunakan aplikasi.

## Struktur Folder Proyek

```
sistem-klasifikasi-deteksi/
├── .venv/                    # Virtual environment
├── .env                      # Konfigurasi environment (lokal)
├── requirements.txt          # Daftar dependensi
├── edudetect.py              # Aplikasi utama Streamlit
├── model/                    # Model YOLO yang telah dilatih
│   ├── best.pt
│   └── ...
├── sections/                 # Modul-modul aplikasi
│   ├── hero.py
│   ├── tentang.py
│   ├── fitur.py
│   ├── upload.py
│   ├── hasil.py
│   └── summary.py
├── utils/                    # Helper functions
│   ├── video_processor.py
│   └── utils.py
└── README.md                 # Dokumentasi aplikasi
```

## Teknologi yang Digunakan

- **Framework**: Streamlit
- **Machine Learning**: YOLOv11 (You Only Look Once v11)
- **AI/NLP**: Google Gemini API (gemini-3-flash-preview)
- **Bahasa Pemrograman**: Python

## Lisensi

MIT License
