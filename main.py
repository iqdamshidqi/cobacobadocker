"""
Pipeline Data Analytics Sederhana
Praktikum Big Data Week 1: Tradisional (Tanpa Docker) vs Docker
"""

import os
import sys
import platform
from pathlib import Path
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Muat environment variable dari file .env jika ada (berguna saat dev lokal)
load_dotenv()

def print_banner(title: str):
    print("\n" + "=" * 60)
    print(f" {title.upper()} ")
    print("=" * 60)

def display_environment_info():
    print_banner("1. Informasi Lingkungan Sistem (Runtime Environment)")
    print(f"• Sistem Operasi (OS)   : {platform.system()} ({platform.release()})")
    print(f"• Arsitektur Mesin      : {platform.machine()}")
    print(f"• Versi Python          : {platform.python_version()} ({sys.executable})")
    print(f"• Versi Pandas          : {pd.__version__}")
    print(f"• Versi NumPy           : {np.__version__}")
    
    # Membaca environment variables
    app_env = os.getenv("APP_ENV", "development")
    data_path = os.getenv("DATA_PATH", "sample_data.csv")
    threshold_str = os.getenv("SALES_THRESHOLD", "500000")
    
    print("-" * 60)
    print(f"• APP_ENV (Config)      : {app_env}")
    print(f"• DATA_PATH (Config)    : {data_path}")
    print(f"• SALES_THRESHOLD       : Rp {int(threshold_str):,}")

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        print(f"\n[ERROR] File data '{file_path}' tidak ditemukan!")
        sys.exit(1)
        
    print_banner("2. Membaca & Membersihkan Data (Data Cleaning)")
    df = pd.read_csv(path)
    print(f"Data mentah berhasil dimuat: {len(df)} baris data.\n")
    print("Sample Data Mentah:")
    print(df.to_string(index=False))
    
    # Deteksi missing values
    missing = df.isnull().sum()
    print("\nDeteksi Missing Values (Nilai Kosong):")
    for col, count in missing.items():
        if count > 0:
            print(f"  - Kolom '{col}': {count} nilai kosong")
            
    # Cleaning:
    # 1. Isi discount_percent yang kosong dengan 0
    df["discount_percent"] = df["discount_percent"].fillna(0)
    
    # 2. Isi quantity yang kosong dengan 1
    df["quantity"] = df["quantity"].fillna(1)
    
    # 3. Isi price yang kosong dengan median harga berdasarkan category
    category_median = df.groupby("category")["price"].transform("median")
    df["price"] = df["price"].fillna(category_median).fillna(df["price"].median())
    
    # 4. Parsing tipe data
    df["price"] = df["price"].astype(float)
    df["quantity"] = df["quantity"].astype(int)
    df["discount_percent"] = df["discount_percent"].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    
    # Feature Engineering: Hitung Total Penjualan Bersih
    df["net_unit_price"] = df["price"] * (1 - (df["discount_percent"] / 100))
    df["total_sales"] = df["net_unit_price"] * df["quantity"]
    
    print("\nData Setelah Pembersihan & Kalkulasi Total Sales:")
    display_cols = ["transaction_id", "category", "price", "quantity", "discount_percent", "total_sales"]
    print(df[display_cols].to_string(index=False))
    
    return df

def perform_analytics(df: pd.DataFrame):
    print_banner("3. Agregasi & Analisis Data (Data Analytics)")
    threshold = float(os.getenv("SALES_THRESHOLD", "500000"))
    
    # Agregasi per Kategori menggunakan Pandas
    agg_category = df.groupby("category").agg(
        total_transaksi=("transaction_id", "count"),
        total_penjualan=("total_sales", "sum"),
        rata_rata_penjualan=("total_sales", "mean"),
        total_item_terjual=("quantity", "sum")
    ).reset_index()
    
    # Format angka agar rapi
    agg_category["total_penjualan_fmt"] = agg_category["total_penjualan"].apply(lambda x: f"Rp {x:,.0f}")
    agg_category["rata_rata_fmt"] = agg_category["rata_rata_penjualan"].apply(lambda x: f"Rp {x:,.0f}")
    
    print("Ringkasan Performa Penjualan per Kategori:")
    print(agg_category[["category", "total_transaksi", "total_item_terjual", "total_penjualan_fmt", "rata_rata_fmt"]].to_string(index=False))
    
    # Filter Transaksi Bernilai Tinggi (High Value Transactions)
    high_value_df = df[df["total_sales"] >= threshold]
    print(f"\nTransaksi Bernilai Tinggi (>= Rp {threshold:,.0f}):")
    if not high_value_df.empty:
        print(high_value_df[["transaction_id", "product_name", "category", "total_sales"]].to_string(index=False))
    else:
        print("  Tidak ada transaksi di atas batas threshold.")
        
    # Kalkulasi Statistik menggunakan NumPy
    sales_array = df["total_sales"].to_numpy()
    mean_val = np.mean(sales_array)
    median_val = np.median(sales_array)
    std_val = np.std(sales_array)
    p90_val = np.percentile(sales_array, 90)
    
    print("\nStatistik Metrik Penjualan (NumPy Calculation):")
    print(f"  • Total Keseluruhan Omzet : Rp {np.sum(sales_array):,.2f}")
    print(f"  • Rata-rata Penjualan     : Rp {mean_val:,.2f}")
    print(f"  • Median (Nilai Tengah)   : Rp {median_val:,.2f}")
    print(f"  • Standar Deviasi         : Rp {std_val:,.2f}")
    print(f"  • 90th Percentile         : Rp {p90_val:,.2f}")

def main():
    print("Memulai Eksekusi Pipeline Big Data Analytics...")
    display_environment_info()
    
    data_path = os.getenv("DATA_PATH", "sample_data.csv")
    df = load_and_clean_data(data_path)
    perform_analytics(df)
    
    print_banner("Eksekusi Selesai dengan Sukses")

if __name__ == "__main__":
    main()
