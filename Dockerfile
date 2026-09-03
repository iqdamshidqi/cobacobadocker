# Menggunakan base image resmi Python 3.11 versi slim berbasis Debian Linux
FROM python:3.11-slim

# Mencegah Python membuat file bytecode .pyc dan memastikan log terminal langsung ter-flush (unbuffered)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    DATA_PATH=sample_data.csv \
    SALES_THRESHOLD=500000

# Menentukan working directory di dalam container
WORKDIR /app

# Copy requirements.txt terlebih dahulu untuk memanfaatkan Docker Layer Caching
COPY requirements.txt /app/

# Install dependensi Python tanpa menyimpan cache pip (menghemat ukuran image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh sisa file aplikasi ke dalam container
COPY . /app/

# Perintah default yang akan dijalankan saat container dijalankan
CMD ["python", "main.py"]
