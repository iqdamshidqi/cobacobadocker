# 📊 Studi Kasus: Python Tradisional vs Berbasis Docker (Kolaborasi Tim Lintas OS)

Repositori ini mendemonstrasikan perbandingan nyata antara **menjalankan proyek data analytics Python secara tradisional (tanpa Docker)** dan **berbasis kontainer (menggunakan Docker)** dalam skenario kolaborasi tim lintas sistem operasi (**macOS** dan **Windows**).

---

## 📁 Struktur Repositori

```text
PRAKTIKUM WEEK 1/
├── sample_data.csv      # Dataset dummy transaksi penjualan (dengan missing values)
├── main.py              # Skrip data analytics (cleaning, pandas aggregation, numpy stats)
├── requirements.txt     # Daftar dependensi yang dikunci untuk Python 3.11
├── Dockerfile           # Instruksi pembuatan image Docker (python:3.11-slim)
├── .dockerignore        # File & folder yang diabaikan saat proses Docker build
├── .env.example         # Template konfigurasi environment variable
├── .gitignore           # File & folder yang diabaikan git
├── README.md            # Dokumentasi utama & tabel komparasi
├── README_MANUAL.md     # 📖 Panduan setup manual (tanpa Docker) & analisis error
└── README_DOCKER.md     # 🐳 Panduan setup berbasis Docker & instruksi build/run
```

---

## 📑 Pilih Panduan Setup

Dokumentasi dibagi menjadi dua panduan terpisah:

| Modus Eksekusi | Berkas Panduan | Deskripsi Ringkas |
| :--- | :--- | :--- |
| **Kasus 1: Tanpa Docker (Manual)** | [👉 Buka README_MANUAL.md](README_MANUAL.md) | Panduan langkah demi langkah membuat virtual environment (`venv`), aktivasi script di Windows (PowerShell/CMD) & macOS, set environment variables, serta bedah studi kasus error kompilasi C++ di Windows (Python 3.13 mismatch). |
| **Kasus 2: Berbasis Docker** | [👉 Buka README_DOCKER.md](README_DOCKER.md) | Panduan instalasi dan eksekusi kontainer dengan perintah universal (identik di macOS dan Windows), passing environment variable runtime, volume mounting, serta bedah isi `Dockerfile`. |

---

## 🔬 Studi Kasus Pipeline Analytics
Aplikasi ini menjalankan pipeline data analytics nyata:
1. Membaca konfigurasi dari environment variables (`APP_ENV`, `DATA_PATH`, `SALES_THRESHOLD`).
2. Menampilkan informasi runtime platform (OS host, arsitektur CPU, versi Python & library).
3. Membaca file CSV mentah dan mendeteksi *missing values*.
4. Membersihkan data (*imputation* harga menggunakan median per kategori, pengisian kuantitas default, parsing tipe data).
5. Melakukan rekayasa fitur (*net unit price* dan *total sales*).
6. Mengelompokkan dan mengagregasi omzet per kategori produk menggunakan Pandas.
7. Memfilter transaksi bernilai tinggi (*high-value transactions*) di atas ambang batas.
8. Menghitung metrik statistik (Mean, Median, Standar Deviasi, dan 90th Percentile) menggunakan NumPy.

---

## ⚖️ Tabel Komparasi Head-to-Head

| Dimensi Evaluasi | Tradisional (Tanpa Docker) | Berbasis Docker |
| :--- | :--- | :--- |
| **Konsistensi Runtime** | Bergantung pada versi Python yang terpasang di OS host pengguna (rentan mismatch misal 3.11 vs 3.13). | **Pasti identik**: Terkunci pada `python:3.11-slim` di semua mesin. |
| **Ketergantungan OS (OS Dependency)** | Sering membutuhkan compiler C++ lokal (Visual C++ Build Tools di Windows, Xcode Command Line Tools di Mac). | **Bebas ketergantungan**: Seluruh dependensi binary dikompilasi di lingkungan Linux kontainer. |
| **Waktu Onboarding Developer** | **Lama**: Butuh instalasi manual, konfigurasi PATH, pembuatan venv, penyelarasan versi pip & OS. | **Sangat Cepat**: Cukup jalankan `docker build` dan `docker run`. |
| **Manajemen Environment Variable** | Berbeda sintaks di setiap shell (`export`, `$env:`, `set`). | **Standar & Terpadu**: Menggunakan flag `-e` atau `--env-file`. |
| **Isolasi Lingkungan** | Isolasi parsial (hanya paket Python via venv, tidak mengisolasi library C sistem atau OS). | **Isolasi Penuh**: Mengisolasi sistem operasi dasar, sistem file, library C, dan Python runtime. |
| **Slogan Praktis** | *"It works on my machine!"* (Tapi error di mesin teman Anda). | *"Works on every machine that runs Docker."* |
