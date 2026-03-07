# TODO: Sesuaikan logika pencarian elemen berdasarkan struktur HTML dari masing-masing portal berita

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from datetime import datetime

def scrape_articles(link):
    # setup driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(15) 

    try:
        driver.get(link)

        # 1. Ekstrak Judul
        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
        except Exception: 
            title = "Tidak ada judul"
        
        # 2. Ekstrak Konten
        try:
            paragraf_html = driver.find_elements(By.TAG_NAME, "p")
            content = " ".join([p.text for p in paragraf_html]).strip()
        except Exception:
            content = ""

        # 3. Menentukan portal berita langsung dengan mem-parsing URL
        try:
            domain = urlparse(link).netloc
            portal = domain.replace("www.", "")
        except Exception:
            portal = "Unknown"

        # 4. TODO: Implementasikan scraping/parsing untuk tanggal & editor 
        date_sementara = None 
        editor = "Tidak diketahui"

        # 5. Membentuk dictionary sesuai Kontrak Data 
        data_artikel = {
            "title": title,
            "date": date_sementara,
            "portal": portal,
            "editor": editor,
            "content": content
        }

    except Exception as e:
        print(f"Gagal membuka web: {link}\nError: {e}")
        data_artikel = None

    driver.quit()
    return data_artikel
