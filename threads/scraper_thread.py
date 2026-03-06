from PyQt5.QtCore import QThread, pyqtSignal
from scraper.link_collector import get_article_links
from scraper.article_scraper import scrape_article
from utils.date_filter import filter_by_date
import time

class ScraperThread(QThread):
    progress_signal = pyqtSignal(int) # signal untuk mengirimkan progress scraping (progress bar)
    result_signal = pyqtSignal(list) # signal untuk mengirimkan hasil scraping (list data)
    error_signal = pyqtSignal(str) # signal untuk mengirimkan error (string)

    # inisialisasi thread 
    def __init__(self, url, limit, start_date=None, end_date=None):
        super().__init__() # memanggil konstruktor QTread
        self.url = url # url yang akan di scrape
        self.limit = limit # batas jumlah artikel yang akan di scrape
        self.start_date = start_date # filter tanggal, mulai
        self.end_date = end_date # filter tanggal, akhir
    
    def run(self):
        try:
            # ambil semua link article
            links = get_article_links(self.url, self.limit) 
            
            # jika tidak ditemukan link artikel yang sesuai, kirimkan error
            if not links:
                self.error_signal.emit("Tidak ditemukan link artikel yang sesuai.") 
                return
            total = len(links)
            scraped_data = []
            
            # scrape setiap link article satu per satu
            for index, link in enumerate(links):
                try:
                    article = scrape_article(link)
                    if article:
                        scraped_data.append(article)
                except Exception as e:
                    print(f"Error scraping {link}: {e}")
                
                # hitung dan kirim progress scraping ke main thread untuk update progress bar
                progress = int((index+1) / total * 100)
                self.progress_signal.emit(progress)
                
                # delay agar tidak membebani server
                time.sleep(0.5)
                
            # filter tanggal
            if self.start_date and self.end_date:
                scraped_data = filter_by_date(scraped_data, self.start_date, self.end_date)
                
            # kirim hasil scraping ke GUI
            self.result_signal.emit(scraped_data)
        
        # mengirim error ke GUI jika terjadi kesalahan selama scrapping    
        except Exception as e:
            self.error_signal.emit(str(e))