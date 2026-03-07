# PERCOBAAN INISIASI PROYEK NEWS SCRAPER APP
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLineEdit, QTableWidget,QFileDialog
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
        self.export_button = QPushButton("Export CSV")

        self.table = QTableWidget()

        layout.addWidget(self.url_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.table)
        

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.export_button.clicked.connect(self.export_to_csv)
    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "CSV Files (*csv)"
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for row in range(self.table.rowCount()):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)