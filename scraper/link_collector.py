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