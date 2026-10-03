# Peta Ekspor Pertanian dan Pangan Indonesia

Proyek ini adalah sebuah dashboard interaktif yang memvisualisasikan data ekspor sektor pertanian dan pangan Indonesia. Aplikasi ini dibuat sebagai pemenuhan tugas Ujian Akhir Semester mata kuliah Visualisasi Data dan Informasi di Politeknik Statistika STIS tahun 2026. Dashboard ini ditujukan untuk memberikan gambaran mengenai struktur komoditas, arah aliran perdagangan, dan seberapa besar ketergantungan ekspor pangan Indonesia terhadap negara-negara tertentu.

![Tangkapan Layar Dashboard](docs/screenshots/hero.png)
*(Catatan: Gambar tangkapan layar di atas masih berupa tautan kosong dan perlu diisi dengan berkas yang sesuai)*

## Fitur Utama

Dashboard ini terdiri dari satu halaman utama yang dibagi menjadi beberapa bagian analisis:

1. **Ringkasan (Hero)**
   Menampilkan metrik utama seperti total nilai ekspor, komoditas penyumbang terbesar, jumlah negara tujuan, dan persentase pertumbuhan dari tahun sebelumnya. Terdapat kontrol untuk memilih tahun data (2023, 2024, atau 2025).

2. **Struktur Komoditas (Hierarki)**
   Menggunakan visualisasi Treemap dan Sunburst untuk membedah komposisi nilai ekspor dari tingkat kelompok, komoditas, hingga negara tujuan pembeli. Warna pada visualisasi menunjukkan persentase perubahan nilai ekspor dibandingkan tahun lalu. Terdapat pengaturan interaktif untuk menyembunyikan komoditas minyak sawit dan menyesuaikan jumlah rincian negara tujuan tiap komoditas (5, 10, atau 20 negara).

3. **Aliran Perdagangan (Aliran)**
   Melacak ke mana komoditas diekspor menggunakan diagram Sankey dan Peta Aliran Geospasial (Flow Map). Pengguna dapat mengatur ambang persentase kontribusi komoditas dan membatasi jumlah negara tujuan teratas untuk menyaring informasi dan mengurangi kepadatan visual.

4. **Jaringan Negara Tujuan (Jaringan)**
   Menganalisis keterkaitan antara komoditas dengan negara mitranya menggunakan Force-Directed Bipartite Graph yang dapat diproyeksikan ke peta geospasial, serta matriks hubungan (Adjacency Matrix). Visualisasi ini menunjukkan nilai sentralitas suatu titik. Terdapat pengaturan ambang nilai minimum dalam juta USD dan opsi untuk menyorot hubungan secara spesifik.

## Struktur Direktori

```text
.
├── .streamlit/             # Konfigurasi antarmuka Streamlit
├── assets/
│   └── hero.jpg            # Gambar latar untuk bagian atas dashboard
├── data/
│   ├── mapping/            # Data pemetaan referensi
│   ├── processed/          # Data CSV olahan akhir yang siap dibaca aplikasi
│   │   ├── chapter_negara_tahun.csv
│   │   ├── chapter_tahun.csv
│   │   ├── ekspor_hs2_detail.csv
│   │   ├── ekspor_hs2_tahun_negara_pelabuhan.csv
│   │   └── negara_tahun.csv
│   └── raw/                # Data mentah awal
├── docs/
│   └── screenshots/        # Tempat menyimpan gambar tangkapan layar aplikasi
├── src/
│   ├── pipeline/           # Skrip pemrosesan data
│   ├── views/              # Berkas perender masing-masing komponen visual
│   │   ├── aliran.py
│   │   ├── hierarki.py
│   │   └── jaringan.py
│   ├── data.py             # Fungsi untuk memuat data olahan dengan metode cache
│   └── style.py            # Modul pengaturan tata letak, gaya CSS, dan kontrol helper
├── app.py                  # Skrip utama untuk menjalankan dashboard
└── requirements.txt        # Daftar dependensi pustaka Python
```

## Cara Menjalankan Aplikasi Secara Lokal

Pastikan Anda sudah menginstal Python. Langkah-langkah menjalankannya adalah sebagai berikut:

1. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di Linux/Mac:
   source venv/bin/activate
   ```
2. Instal pustaka yang dibutuhkan dari `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```

Aplikasi dapat diakses melalui peramban web pada alamat `http://localhost:8501`.

## Tentang Data

Sumber data yang digunakan adalah tabel Ekspor HS 2 Digit dari Badan Pusat Statistik (BPS) untuk tahun 2023, 2024, dan 2025. Data mencakup kelompok komoditas HS chapter 01 hingga 24 menurut negara tujuan, pelabuhan, dan bulan, dengan satuan ukur USD. Data diakses pada 3 Oktober 2026 melalui tautan https://www.bps.go.id/id/exim. 

Aplikasi langsung membaca file CSV olahan yang berada di dalam folder `data/processed/`. File tersebut dimuat oleh modul `src/data.py` dengan memanfaatkan sistem penyimpanan sementara atau cache dari Streamlit agar pembacaan tabel berjalan lebih efisien.

## Keterbatasan

Terdapat beberapa batasan dalam analisis visualisasi ini:
- Analisis hanya dilakukan pada tingkat chapter, bukan pada komoditas rinci.
- Nama kelompok komoditas adalah ringkasan buatan penulis, bukan nama resmi dari BTKI.
- Pengaturan ambang nilai batas dan jumlah negara teratas memengaruhi tampilan visualisasi pada kelompok Aliran dan Jaringan.

## Penggunaan Alat AI

Asisten AI dipakai untuk membantu menulis, men-debug kode, serta keperluan teknis dalam pengkodingan. Seluruh data, angka, rancangan visual, dan hasil dibuat, diperiksa, dan dipahami sendiri oleh penulis.

## Kredit dan Lisensi

- Gambar hero diambil dari [Pinterest](https://id.pinterest.com/pin/966936982510692087/).
