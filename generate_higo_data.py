import pandas as pd
import numpy as np
import random
import scipy.stats as st
from datetime import datetime

# Pengaturan Seed agar hasil data konsisten setiap kali dijalankan
np.random.seed(42)
random.seed(42)

n_data = 1000

# --- Persiapan Data Master (Dummy) ---
first_names = ['Budi', 'Siti', 'Andi', 'Dewi', 'Joko', 'Rina', 'Agus', 'Maya', 'Eko', 'Sari', 'Rahmat', 'Ani', 'Hendra', 'Yanti', 'Dedi', 'Lusi', 'Bambang', 'Wati', 'Taufik', 'Ika']
last_names = ['Santoso', 'Prasetyo', 'Wijaya', 'Kusuma', 'Putra', 'Putri', 'Hidayat', 'Lestari', 'Saputra', 'Ramadhan', 'Gunawan', 'Suryani', 'Wibowo', 'Kartika', 'Setiawan']
domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']

tipe_lokasi_list = ['Pusat Perbelanjaan', 'Kafe & Restoran', 'Transportasi Publik', 'Kampus']
lokasi_dict = {
    'Pusat Perbelanjaan': ['Mall Grand Indonesia', 'Pondok Indah Mall', 'Senayan City'],
    'Kafe & Restoran': ['Kopi Kenangan Senopati', 'Starbucks Sudirman', 'Janji Jiwa Kemang'],
    'Transportasi Publik': ['Stasiun MRT Bundaran HI', 'Stasiun KRL Sudirman', 'Halte TransJakarta Blok M'],
    'Kampus': ['Universitas Indonesia', 'Binus Anggrek', 'Universitas Tarumanagara']
}
merk_hp_list = ['Apple', 'Samsung', 'Xiaomi', 'Oppo', 'Vivo', 'Realme']
minat_digital_list = ['E-Commerce', 'Gaming', 'Social Media', 'Finance/Investment', 'News/Portal']

data = []

# --- Loop Pembuatan Data ---
for _ in range(n_data):
    tipe_lokasi = random.choice(tipe_lokasi_list)
    nama_lokasi = random.choice(lokasi_dict[tipe_lokasi])
    
    # 1. Jam Login dalam format AM/PM (Sesuai Gambar)
    h = random.randint(0, 23)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    jam_login = datetime.strptime(f"{h:02d}:{m:02d}:{s:02d}", "%H:%M:%S").strftime("%I:%M:%S %p")
    
    # 2. Nama & Email
    fn, ln = random.choice(first_names), random.choice(last_names)
    nama = f"{fn} {ln}"
    email = f"{fn.lower()}{random.randint(10,99)}@{random.choice(domains)}"
    
    # 3. No Telepon dengan format 08XX-XXXX-XXXX
    prefix = random.choice(['0812', '0813', '0821', '0852', '0811', '0857', '0818'])
    b1, b2 = "".join([str(random.randint(0, 9)) for _ in range(4)]), "".join([str(random.randint(0, 9)) for _ in range(4)])
    no_telp = f"{prefix}-{b1}-{b2}"
    
    tahun_lahir = random.randint(1980, 2008) 
    merk_hp = random.choice(merk_hp_list)
    kategori_minat = random.choice(minat_digital_list)
    skor_minat_digital = random.randint(50, 100) 
    
    data.append([nama_lokasi, jam_login, nama, email, no_telp, tahun_lahir, merk_hp, kategori_minat, skor_minat_digital, tipe_lokasi])

# Membuat DataFrame
df = pd.DataFrame(data, columns=['Nama Lokasi', 'Jam Login', 'Nama', 'Email', 'No Telepon', 'Tahun Lahir', 'Merk HP', 'Kategori Minat Digital', 'Skor Minat Digital', 'Tipe Lokasi'])

# --- 3. Feature Engineering (Variabel Baru) ---
df['Usia'] = 2026 - df['Tahun Lahir']
df['Generasi'] = df['Tahun Lahir'].apply(lambda x: 'Gen X' if x <= 1980 else ('Milenial' if x <= 1996 else 'Gen Z'))

def get_session(jam_str):
    hour = datetime.strptime(jam_str, "%I:%M:%S %p").hour
    if 5 <= hour < 12: return 'Pagi'
    elif 12 <= hour < 15: return 'Siang'
    elif 15 <= hour < 19: return 'Sore'
    else: return 'Malam'

df['Sesi Login'] = df['Jam Login'].apply(get_session)
df['Provider Email'] = df['Email'].apply(lambda x: x.split('@')[1])

# --- 4. Perhitungan Confidence Interval (Nilai Plus) ---
def get_ci(data_series, confidence=0.95):
    n = len(data_series)
    mean = np.mean(data_series)
    sem = st.sem(data_series)
    h = sem * st.t.ppf((1 + confidence) / 2, n - 1)
    return mean, mean - h, mean + h

m_skor, low_skor, up_skor = get_ci(df['Skor Minat Digital'])
m_usia, low_usia, up_usia = get_ci(df['Usia'])

# --- Finalisasi & Ekspor ---
df.to_csv('data_dummy_higo_final.csv', index=False)

print("--- Hasil Analisis Statistik (Confidence Interval 95%) ---")
print(f"Rata-rata Skor Minat: {m_skor:.2f} (Rentang CI: {low_skor:.2f} s/d {up_skor:.2f})")
print(f"Rata-rata Usia: {m_usia:.2f} (Rentang CI: {low_usia:.2f} s/d {up_usia:.2f})")
print("\n[SUCCESS] File 'data_dummy_higo_final.csv' telah berhasil dibuat.")