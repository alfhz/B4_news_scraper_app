# 📰 News Scraper GUI App

Aplikasi desktop untuk scraping berita menggunakan Python, Selenium, dan PyQt5.

Aplikasi ini dapat:
- Mengambil link artikel dari halaman berita (termasuk pagination)
- Mengambil detail artikel (judul, tanggal, isi, portal, editor)
- Membatasi jumlah berita (limit)
- Filter berdasarkan rentang tanggal
- Menampilkan progress bar saat scraping
- Export hasil ke CSV   
- Tidak freeze (menggunakan threading)

---

# 👥 SETUP UNTUK SEMUA ANGGOTA TIM

Ikuti langkah ini dari awal sampai selesai.

---

# 1️⃣ Clone Repository

Buka CMD / Git Bash lalu jalankan:

    git clone https://github.com/USERNAME/B4_news_scraper_app.git

Masuk ke folder project:

    cd B4_news_scraper_app

---

# 2️⃣ Buat Virtual Environment

Buat environment baru:

    python -m venv venv

Aktifkan:

Windows (CMD):
    venv\Scripts\activate

Windows (Git Bash):
    source venv/Scripts/activate

Jika berhasil, akan muncul `(venv)` di awal terminal.

---

# 3️⃣ Install Dependency

Install semua library yang dibutuhkan:

    pip install -r requirements.txt

Pastikan tidak ada error.

---

# 4️⃣ Test Jalankan Aplikasi

    python main.py

Jika window aplikasi muncul → setup berhasil ✅

---

# 5️⃣ WAJIB Buat Branch Masing-Masing

⚠ DILARANG kerja langsung di branch `main`.

Buat branch sesuai nama masing-masing (huruf kecil semua):

    git branch nama
    git checkout nama


Cek branch aktif:

    git branch

Branch dengan tanda `*` adalah branch aktif.

---

# 6️⃣ Workflow Kerja Harian

Setiap selesai kerja:

    git add .
    git commit -m "Deskripsi perubahan"
    git push origin nama-branch

Contoh:

    git push origin scraper-link

---

# 7️⃣ Update dari Main (Jika Diperlukan)

Jika branch `main` sudah di-update oleh anggota lain:

    git checkout main
    git pull origin main
    git checkout nama-branch
    git merge main

Jika ada konflik → diskusikan dulu sebelum resolve.

---

# 🚫 ATURAN PENTING

- ❌ Jangan kerja di branch main
- ❌ Jangan ubah struktur folder tanpa diskusi
- ❌ Jangan ubah kontrak data
- ❌ Jangan push folder venv
- ❌ Jangan push file __pycache__
- ❌ Jangan merge tanpa testing minimal

---

# 📂 Struktur Proyek

B4_news_scraper_app/
│
├── main.py
│
├── gui/
│   └── main_window.py
│
├── scraper/
│   ├── link_collector.py
│   └── article_scraper.py
│
├── threads/
│   └── scraper_thread.py
│
├── utils/
│   ├── export.py
│   └── date_filter.py
│
├── requirements.txt
├── README.md
└── .gitignore

---

# 📦 Dependency

Library yang digunakan:
- PyQt5
- selenium
- pandas
- python-dateutil

Semua akan terinstall otomatis dengan:

    pip install -r requirements.txt

---

# 📊 Kontrak Data Artikel (WAJIB)

Semua artikel harus berbentuk:

    {
      "title": str,
      "date": datetime | None,
      "content": str,
      "portal": str,
      "editor": str
    }

⚠ date HARUS bertipe datetime, bukan string.  
⚠ Jika parsing gagal → date = None.

---

# 🎯 Target Akhir Project

Aplikasi harus bisa:

- Input URL berita
- Ambil link artikel + pagination
- Ambil title, date(datetime), content, portal, editor
- Batasi jumlah berita (limit)
- Filter berdasarkan tanggal
- Tampilkan progress bar
- Export CSV
- Tidak freeze
- Tidak crash

---

# 🔥 Attention!

- Commit kecil tapi sering
- Jangan tunggu file selesai 100% baru commit
- Update branch secara berkala
- Diskusi sebelum merge
- Jaga format data tetap konsisten

---
