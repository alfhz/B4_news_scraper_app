from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_article_links(url, limit):
    print(f"[{time.strftime('%H:%M:%S')}] Mengumpulkan link dari: {url} (Limit: {limit})")
    
    # Konfigurasi Headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Gunakan User-Agent asli agar tidak diblokir
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    collected_links = set()
    
    try:
        driver.get(url)
        time.sleep(2)  # Tunggu page load awal

        scroll_attempts = 0
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(collected_links) < limit and scroll_attempts < 10:
            # Ambil semua link menggunakan JavaScript agar jauh lebih cepat (tidak membuat aplikasi hang)
            hrefs = driver.execute_script("return Array.from(document.querySelectorAll('a')).map(a => a.href);")
            for href in hrefs:
                # Filter kasar untuk memastikan ini link dari situs berita
                if href and href.startswith("http") and ("/" in href.replace("https://", "").replace("http://", "")):
                    # Hindari link ke home, kategori utama / tag saja
                    if len(href.split('/')) > 4: 
                        collected_links.add(href)
                        if len(collected_links) >= limit:
                            break
                            
            if len(collected_links) >= limit:
                break
            
            # Scroll ke bawah untuk mencoba lazy-load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_height = new_height

    except Exception as e:
        print(f"Error saat mengumpulkan link: {e}")
    finally:
        driver.quit()
        
    result_list = list(collected_links)[:limit]
    print(f"[{time.strftime('%H:%M:%S')}] Ditemukan {len(result_list)} link target.")
    return result_list
