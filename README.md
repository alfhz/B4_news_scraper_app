# 📰 News Scraper App (PyQt5)

Aplikasi desktop berbasis **Python + PyQt5** untuk melakukan **scraping artikel berita secara otomatis** dari halaman portal berita.  
Aplikasi ini menyediakan antarmuka GUI yang memungkinkan pengguna mengambil artikel, memfilter berdasarkan tanggal, dan mengekspor hasilnya ke file CSV.

---

# Fitur Utama

- **Input URL Berita**
  - Pengguna dapat memasukkan link halaman berita yang ingin di-scrape.

- **Limit Artikel**
  - Mengatur jumlah maksimal artikel yang akan diambil.

- **Filter Rentang Tanggal**
  - Mengambil artikel hanya dalam rentang tanggal tertentu.

- **Threaded Scraping**
  - Menggunakan `QThread` agar GUI tidak freeze saat proses scraping berjalan.

- **Progress Monitoring**
  - Progress bar menampilkan perkembangan proses scraping secara real-time.

- **Tabel Hasil Scraping**
  - Menampilkan:
  - Nomor
  - Judul Artikel
  - Tanggal
  - Portal
  - Editor
  - Preview isi artikel

- **Export ke CSV**
  - Data hasil scraping dapat disimpan sebagai file `.csv`.

---

# Tampilan Aplikasi

Aplikasi memiliki beberapa bagian utama:

| Bagian | Deskripsi |
|------|------|
| Header | Judul aplikasi dan deskripsi |
| Input Panel | URL berita, limit artikel, dan filter tanggal |
| Progress Section | Progress bar proses scraping |
| Table Section | Tabel hasil artikel yang ditemukan |
| Status Bar | Informasi status proses scraping |

---
# Screenshot Aplikasi

'tampilanApp.png'
'tampilanApp2.png'

# Struktur Project

Berikut struktur folder utama project:

```
B4_news_scraper_app
│
├── main.py
│
├── gui
│   ├── __init__.py
│   ├── main_window.py
│   └── style.qss
│
├── threads
│   └── scraper_thread.py
│
├── scraper
│   └── article_scraper.py
│
├── utils
│
└── README.md
```

### Penjelasan Folder

| Folder | Fungsi |
|------|------|
| gui | Berisi kode GUI PyQt5 |
| threads | Thread untuk menjalankan proses scraping |
| scraper | Logic scraping artikel |
| utils | Fungsi tambahan / helper |
| main.py | Entry point aplikasi |

---

# Teknologi yang Digunakan

- **Python 3**
- **PyQt5** → GUI Framework
- **Selenium** → Scrapper
- **Requests** → HTTP request
- **BeautifulSoup4** → HTML parsing
- **CSV module** → Export data
- **python-dateutil** → Date
- **QThread** → Asynchronous processing

---

# Instalasi

## 1. Clone Repository

```bash
git clone https://github.com/alfhz/B4_news_scraper_app.git
cd B4_news_scraper_app
```

---

## 2. Buat Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install PyQt5 selenium requests beautifulsoup4 python-dateutil
```

---

# ▶Menjalankan Aplikasi

Jalankan aplikasi dengan perintah:

```bash
python main.py
```

GUI aplikasi akan muncul dan siap digunakan.

---

# Cara Menggunakan Aplikasi

1. Masukkan **URL halaman berita** pada kolom input.
2. Tentukan **limit jumlah artikel** yang ingin diambil.
3. Pilih **rentang tanggal artikel**.
4. Klik **Start Scraping**.
5. Tunggu hingga progress selesai.
6. Hasil artikel akan muncul di tabel.
7. Klik **Export CSV** untuk menyimpan data.

---

# Format Output CSV

File CSV akan berisi kolom berikut:

```
title,date,portal,editor,content
```

Contoh:

```
Judul Berita,2024-05-02,Isi artikel...,detik.com,Editor A
```

---


# Pengembang

**Alifah Zachra Syifatunnajwa**  
**Alfina Azizah**  
**Haidar Azka**  
**Muhammad Fawwaz Muzaki**  
**Nadhief Musyaffa**  
Jurusan Teknik Informatika  
Politeknik Negeri Bandung (POLBAN)

---

# Lisensi

Proyek ini dibuat untuk keperluan **pembelajaran dan praktikum**.