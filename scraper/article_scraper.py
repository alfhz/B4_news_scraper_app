# TODO: implement scrape_articles()
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

def scrape_article(url):
    # implementasi fungsi untuk mengambil data artikel dari link yang diberikan
    # buka halaman artikel menggunakan Selenium
    # ambil data berikut:
        # - judul artikel
        # - tanggal artikel
        # - portal berita
        # - editor (kalo ga ada default anonym)
        # - isi artikel
    # validasi data yang diambil
        # - Jika title kosong → skip artikel.
        # - Jika content kosong → skip.
        # - Jika editor tidak ditemukan → isi `"Annonym"`.
        # - Delay antar artikel.
        # - Semua akses elemen pakai try-except.
    # kembalikan data artikel dalam bentuk dictionary
    
    # dummy data untuk testing
    article = {
        "title": "Contoh Judul Berita",
        "date": datetime(2026, 3, 6),
        "portal": "Example News",
        "editor": "Admin",
        "content": "Ini isi berita contoh",
    }

    return article