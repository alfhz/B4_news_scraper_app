from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin
import time


def get_article_links(url, limit):
    """
    Mengambil semua link artikel dari halaman berita (homepage/kategori).
    Mendukung pagination otomatis dan limit jumlah link.

    Parameters:
        url   (str): URL halaman berita utama / kategori.
        limit (int): Batas maksimal jumlah link yang dikumpulkan.

    Returns:
        list[str]: Daftar URL artikel unik, maksimal sejumlah limit.
    """
    driver = None
    collected_links = []
    visited_pages = set()

    try:
        # Setup headless Chrome
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)