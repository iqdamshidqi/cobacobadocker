# 🐳 Panduan Setup 

---

## 📋 Prasyarat Sistem
- **Docker Desktop** (sudah terinstal dan berstatus *Running*):
  - [Unduh Docker Desktop untuk Windows / Mac](https://www.docker.com/products/docker-desktop/)
- Verifikasi instalasi di terminal:
  ```bash
  docker --version
  ```

---

## 🔍 Anatomi Konfigurasi Docker

### 1. Bedah File `Dockerfile`
Setiap baris di dalam [`Dockerfile`](file:///Volumes/Iqdam%20Drive/MATKUL%20SEMESTER%205/Big%20Data/PRAKTIKUM%20WEEK%201/Dockerfile) memiliki tujuan spesifik:

```dockerfile
# 1. Base image resmi Python 3.11 versi slim berbasis Debian Linux (ringan dan stabil)
FROM python:3.11-slim

# 2. Pengaturan environment untuk performa container:
#    - Mencegah file bytecode .pyc
#    - Memastikan output terminal tidak ter-buffer sehingga log muncul real-time
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    DATA_PATH=sample_data.csv \
    SALES_THRESHOLD=500000

# 3. Direktori kerja di dalam kontainer
WORKDIR /app

# 4. Memanfaatkan Docker Layer Caching:
#    Hanya install ulang library jika file requirements.txt berubah
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Salin seluruh sisa file proyek ke dalam kontainer
COPY . /app/

# 6. Perintah default saat kontainer dijalankan
CMD ["python", "main.py"]
```

### 2. Fungsi File `.dockerignore`
File [`.dockerignore`](file:///Volumes/Iqdam%20Drive/MATKUL%20SEMESTER%205/Big%20Data/PRAKTIKUM%20WEEK%201/.dockerignore) memastikan file-file yang tidak relevan (seperti `venv/`, `__pycache__/`, `.git`, `.DS_Store`, dan `.env` lokal) **tidak ikut tersalin** ke dalam image Docker. Hal ini membuat proses build jauh lebih cepat dan ukuran image menjadi lebih ramping.

---

## 🚀 Langkah Eksekusi (Build & Run)

### 1. Membangun Docker Image (Build)
Buka terminal di direktori proyek ini, lalu jalankan:
```bash
docker build -t bigdata-analytics:1.0 .
```
> 💡 *Arti argumen:*  
> `-t bigdata-analytics:1.0` memberikan nama (*tag*) image.  
> `.` (titik di akhir) merujuk ke direktori saat ini sebagai build context.

---

### 2. Menjalankan Kontainer (Default Run)
Setelah image selesai dibuat, jalankan aplikasi dengan perintah:
```bash
docker run --rm bigdata-analytics:1.0
```
> 💡 *Arti flag `--rm`:*  
> Menghapus kontainer secara otomatis setelah selesai dieksekusi agar tidak memenuhi memori penyimpanan.

---

### 3. Menjalankan dengan Custom Environment Variables
Salah satu keunggulan Docker adalah Anda dapat mengubah parameter konfigurasi tanpa perlu mengubah kode atau membangun ulang (*rebuild*) image Docker:

```bash
docker run --rm -e APP_ENV=staging -e SALES_THRESHOLD=1000000 bigdata-analytics:1.0
```
Pada contoh di atas, threshold penjualan diubah menjadi **Rp 1.000.000** secara langsung saat runtime.

---

### 4. Volume Mounting (Sinkronisasi Data Real-Time)
Jika Anda ingin mengubah file `sample_data.csv` di komputer host Anda dan langsung melihat hasil perhitungannya tanpa perlu menjalankan `docker build` ulang:

#### A. Pada macOS / Linux (Zsh / Bash):
```bash
docker run --rm -v "$(pwd)/sample_data.csv:/app/sample_data.csv" bigdata-analytics:1.0
```

#### B. Pada Windows (PowerShell):
```powershell
docker run --rm -v "${PWD}/sample_data.csv:/app/sample_data.csv" bigdata-analytics:1.0
```

#### C. Pada Windows (Command Prompt / CMD):
```cmd
docker run --rm -v "%cd%/sample_data.csv:/app/sample_data.csv" bigdata-analytics:1.0
```

---

### 5. Masuk ke Shell Interaktif Kontainer (Debugging)
Jika Anda ingin mengecek isi direktori atau menjalankan Python REPL di dalam kontainer Linux:
```bash
docker run --rm -it bigdata-analytics:1.0 /bin/bash
```
Di dalam bash kontainer, Anda bisa menjalankan `ls -la`, `python`, atau inspeksi data secara langsung. Ketik `exit` untuk keluar.

---

