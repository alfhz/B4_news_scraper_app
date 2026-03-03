# PERCOBAAN INISIASI PROYEK NEWS SCRAPER APP
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLineEdit, QTableWidget
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News Scraper App")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL berita")

        self.start_button = QPushButton("Start Scraping")

        self.table = QTableWidget()

        layout.addWidget(self.url_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.table)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)