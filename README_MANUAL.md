# 🛠️ Panduan Setup

---

## 📋 Prasyarat Sistem
- **Python 3.11** (Sangat disarankan).
- **pip** (Package installer for Python).
- Terminal:
  - Windows: **PowerShell** atau **Command Prompt (CMD)**.
  - macOS/Linux: **Zsh** atau **Bash**.

---

## 🪟 1. Panduan Setup Manual di Windows

### Langkah 1: Buka Terminal & Verifikasi Python
Buka PowerShell atau CMD, lalu periksa versi Python:
```powershell
python --version
```
> ⚠️ **Peringatan Versi:** Jika versi Python Anda adalah **Python 3.13** atau lebih baru, library seperti `numpy 1.26.4` kemungkinan besar akan gagal dipasang karena belum tersedianya *binary wheel* siap pakai untuk Windows (lihat bagian [Studi Kasus Error](#-studi-kasus-error-nyata-di-windows)).

### Langkah 2: Buat Virtual Environment
Buat virtual environment terisolasi bernama `venv`:
```powershell
python -m venv venv
```

### Langkah 3: Aktivasi Virtual Environment

#### Pilihan A: Menggunakan PowerShell (Direkomendasikan)
```powershell
.\venv\Scripts\Activate.ps1
```
> 🛑 **Troubleshooting Error Execution Policy di PowerShell:**  
> Jika muncul pesan error merah:
> ```text
> File ...\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
> ```
> **Solusi:** Izinkan eksekusi skrip hanya untuk sesi terminal saat ini dengan menjalankan:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\venv\Scripts\Activate.ps1
> ```

#### Pilihan B: Menggunakan Command Prompt (CMD)
```cmd
venv\Scripts\activate.bat
```

Setelah aktif, prompt terminal Anda akan memiliki tanda awalan `(venv)`.

### Langkah 4: Set Environment Variables
Konfigurasikan variabel lingkungan sebelum menjalankan script:

* **Di PowerShell:**
  ```powershell
  $env:APP_ENV="development"
  $env:DATA_PATH="sample_data.csv"
  $env:SALES_THRESHOLD="500000"
  ```
  *(Untuk memeriksa nilai variabel di PowerShell: `echo $env:APP_ENV`)*

* **Di CMD:**
  ```cmd
  set APP_ENV=development
  set DATA_PATH=sample_data.csv
  set SALES_THRESHOLD=500000
  ```
  *(Untuk memeriksa nilai variabel di CMD: `echo %APP_ENV%`)*

> 💡 *Alternatif:* Anda juga dapat menyalin `.env.example` menjadi `.env` jika tidak ingin mengetik perintah di terminal:
> ```powershell
> copy .env.example .env
> ```

### Langkah 5: Install Dependensi
Perbarui pip dan pasang library dari `requirements.txt`:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Langkah 6: Jalankan Pipeline Analytics
```powershell
python main.py
```

---

## 🍏 2. Panduan Setup Manual di macOS / Linux

### Langkah 1: Buka Terminal & Verifikasi Python
```bash
python3 --version
```

### Langkah 2: Buat & Aktifkan Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3: Export Environment Variables
```bash
export APP_ENV=development
export DATA_PATH=sample_data.csv
export SALES_THRESHOLD=500000
```
*(Atau salin template: `cp .env.example .env`)*

### Langkah 4: Install Dependensi & Jalankan
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
python main.py
```

---
