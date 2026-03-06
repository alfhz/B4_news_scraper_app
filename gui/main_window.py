# PERCOBAAN INISIASI PROYEK NEWS SCRAPER APP
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLineEdit, QTableWidget, 
)
from threads.scraper_thread import ScraperThread
import json

class MainWindow(QMainWindow):
    # inisialisasi main window
    def __init__(self):
        # membuat tampilan GUI aplikasi
        # menyediakan input untuk URL berita dari user
        # menyediakan tombol untuk memulai proses scraping
        # membuat tabel untuk menampilkan hasil scraping
        # ketika tombol start ditekan, panggil ScraperThread
        # menerima signal dari thread untuk:
            # - update progress scraping
            # - menampilkan hasil scraping
            # - menampilkan error jika terjadi kesalahan
        # styling GUI
        # validasi input, jika gagal → tampilkan QMessageBox.warning
            # - URL tidak kosong.
            # - URL diawali `http`.
            # - Limit ≥ 1.
            # - Start date ≤ End date.
        super().__init__()
        self.setWindowTitle("News Scraper App")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        # field input url
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL berita")

        # tombol start 
        self.start_button = QPushButton("Start Scraping")

        # tabel hasil scraping
        self.table = QTableWidget()

        layout.addWidget(self.url_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.table)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # koneksi tombel start ke fungsi start_scraping
        self.start_button.clicked.connect(self.start_scraping)
        
    # implementasi thread untuk menangani proses scraping agar GUI tetap responsif
    # fungsi untuk memulai proses scraping ketika tombol start ditekan
    def start_scraping(self):
        # pengambilan input url dan parameter limit, start_date, dan end_date dari GUI
        url = self.url_input.text()
        limit = 10
        start_date = None
        end_date = None
        
        # inisialisasi thread scraper dengan parameter yang diambil dari GUI
        self.thread = ScraperThread(url, limit, start_date, end_date)
        # koneksi signal untuk menangani progress, hasil, dan error dari thread scraper
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.result_signal.connect(self.show_results)
        self.thread.error_signal.connect(self.show_error)
        # thread scraper dijalankan
        self.thread.start()
        
    # menangani update progress dari thread scraper (progress bar)     
    def update_progress(self, progress):
        print("Progress: ", progress)
    
    # menangani hasil scraping dari thread scraper (harusnya hasil di tabel)    
    def show_results(self, data):
        print("Hasil Scraping: ", json.dumps(data, indent=4, default=str))
    
    # menangani error saat proses scrapping (error message)    
    def show_error(self, message):
        print("Error: ", message)