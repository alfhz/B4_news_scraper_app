import time
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraper.link_collector import get_article_links
from scraper.article_scraper import scrape_articles

class ScraperThread(QThread):
    progress_signal = pyqtSignal(int) # buat update progress bar
    result_signal = pyqtSignal(list) # kirim list hasil ke tabel
    error_signal = pyqtSignal(str) # kirim pesan error

    def __init__(self, url, limit, start_date=None, end_date=None):
        super().__init__()
        self.url = url 
        self.limit = limit 
        self.start_date = start_date 
        self.end_date = end_date 
        self.is_terminated = False 
    
    def run(self):
        # setup driver sekali di awal biar efisien
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # ambil link cadangan agak banyakan (50) biar bisa difilter
            links = get_article_links(self.url, 50) 
            
            if not links:
                self.error_signal.emit("Link artikel tidak ditemukan sama sekali.") 
                return
                
            scraped_data = []
            link_index = 0
            
            # loop terus sampe limit terpenuhi atau link abis
            while len(scraped_data) < self.limit and link_index < len(links):
                if self.is_terminated:
                    break
                
                link = links[link_index]
                article = scrape_articles(link, driver)
                
                if article:
                    art_date = article.get("date")
                    # cek range tanggal
                    if self.start_date.date() <= art_date <= self.end_date.date():
                        scraped_data.append(article)
                        print(f"      [OK] Berhasil scrapping ({len(scraped_data)}/{self.limit})")
                    else:
                        print(f"      [SKIP] Tanggal tidak masuk kriteria.")
                else:
                    print(f"      [SKIP] Bukan artikel atau konten kosong.")

                # progress bar ngikutin seberapa deket ke target limit
                progress = int((len(scraped_data) / self.limit) * 100)
                self.progress_signal.emit(progress)
                
                link_index += 1
                time.sleep(0.5) # biar gak disangka DDOS
                
            self.result_signal.emit(scraped_data)
            
        except Exception as e:
            self.error_signal.emit(str(e))
        finally:
            driver.quit() # tutup browser kalo udah beres semua
            print(f"[{time.strftime('%H:%M:%S')}] Browser ditutup. Selesai.")

    def terminate_thread(self):
        self.is_terminated = True