# TODO: implement get_article_links()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_article_links(url, limit):
    # implementasi fungsi untuk mengambil semua link artikel dari halaman berita
    # gunakan Selenium untuk mengambil link artikel
    # jika halaman memiliki pagination, lanjutkan scraping ke halaman berikutnya
    # hentikan proses jika jumlah link sudah mencapai limit
    # kembalikan hasil dalam bentuk list berisi URL artikel
    
    # dummy data untuk testing
    return [
        "https://example.com/article1",
        "https://example.com/article2",
        "https://example.com/article3",
    ][:limit]