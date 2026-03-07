# PERCOBAAN INISIASI PROYEK NEWS SCRAPER APP
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QLabel, QSpinBox, QDateEdit, QProgressBar, QFileDialog,
    QHeaderView, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from threads.scraper_thread import ScraperThread
import json
import csv

# ──────────────────────────────────────────────
# STYLING - Alfina Azizah_034
# ──────────────────────────────────────────────
STYLESHEET = """
QMainWindow, QWidget {
    background-color: #0f1923;
    color: #e8edf2;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

#header_panel {
    background-color: #152233;
    border-bottom: 2px solid #1e8bc3;
    padding: 8px 0px;
}

#app_title {
    font-size: 22px;
    font-weight: bold;
    color: #1e8bc3;
    letter-spacing: 1px;
}

#app_subtitle {
    font-size: 11px;
    color: #7a9ab5;
}

#input_panel {
    background-color: #152233;
    border: 1px solid #1e3a52;
    border-radius: 8px;
    padding: 12px;
}

QLabel {
    color: #8fb3cc;
    font-size: 12px;
    font-weight: 600;
}

QLineEdit {
    background-color: #0f1923;
    border: 1px solid #1e3a52;
    border-radius: 5px;
    color: #e8edf2;
    padding: 6px 10px;
    font-size: 13px;
}

QLineEdit:focus { border: 1px solid #1e8bc3; }

QSpinBox, QDateEdit {
    background-color: #0f1923;
    border: 1px solid #1e3a52;
    border-radius: 5px;
    color: #e8edf2;
    padding: 5px 8px;
}

QSpinBox:focus, QDateEdit:focus { border: 1px solid #1e8bc3; }

QSpinBox::up-button, QSpinBox::down-button,
QDateEdit::up-button, QDateEdit::down-button {
    background-color: #1e3a52;
    border: none;
    width: 18px;
}

#btn_start {
    background-color: #1e8bc3;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 9px 22px;
    font-size: 13px;
    font-weight: bold;
}

#btn_start:hover { background-color: #2aa3df; }
#btn_start:disabled { background-color: #1e3a52; color: #4a6a82; }

#btn_stop {
    background-color: #c0392b;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 9px 22px;
    font-size: 13px;
    font-weight: bold;
}

#btn_stop:hover { background-color: #e74c3c; }
#btn_stop:disabled { background-color: #2a1a1a; color: #4a6a82; }

#btn_export {
    background-color: #1a7a4a;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 9px 22px;
    font-size: 13px;
    font-weight: bold;
}

#btn_export:hover { background-color: #22a060; }
#btn_export:disabled { background-color: #0f2a1a; color: #4a6a82; }

QProgressBar {
    background-color: #0f1923;
    border: 1px solid #1e3a52;
    border-radius: 5px;
    height: 16px;
    text-align: center;
    color: #e8edf2;
    font-size: 11px;
}

QProgressBar::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1e5c8b, stop:1 #1e8bc3
    );
    border-radius: 4px;
}

QTableWidget {
    background-color: #0f1923;
    border: 1px solid #1e3a52;
    border-radius: 6px;
    gridline-color: #1e3a52;
    color: #e8edf2;
    font-size: 12px;
}

QTableWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #152233;
}

QTableWidget::item:selected {
    background-color: #1e3a52;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #152233;
    color: #1e8bc3;
    border: none;
    border-right: 1px solid #1e3a52;
    border-bottom: 2px solid #1e8bc3;
    padding: 8px;
    font-weight: bold;
    font-size: 12px;
}

#status_label {
    color: #7a9ab5;
    font-size: 11px;
    padding: 4px 8px;
}

QScrollBar:vertical {
    background: #0f1923;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #1e3a52;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover { background: #1e8bc3; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }

QScrollBar:horizontal {
    background: #0f1923;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: #1e3a52;
    border-radius: 4px;
}
"""


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
        self.setGeometry(100, 100, 1050, 720)
        self.setStyleSheet(STYLESHEET)

        self._articles = []
        self._thread = None

        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_header())

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 14, 16, 10)
        content_layout.setSpacing(12)

        content_layout.addWidget(self._build_input_panel())
        content_layout.addWidget(self._build_progress_section())
        content_layout.addWidget(self._build_table_section())
        content_layout.addWidget(self._build_statusbar())

        root_layout.addWidget(content)
        self.setCentralWidget(root)

    def _build_header(self):
        panel = QWidget()
        panel.setObjectName("header_panel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 10, 20, 10)

        from PyQt5.QtGui import QFont
        icon_label = QLabel("📰")
        icon_label.setFont(QFont("Segoe UI", 20))

        title_col = QVBoxLayout()
        title_col.setSpacing(1)

        title = QLabel("News Scraper App")
        title.setObjectName("app_title")

        subtitle = QLabel("Scraping artikel berita • Filter tanggal • Export CSV")
        subtitle.setObjectName("app_subtitle")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        layout.addWidget(icon_label)
        layout.addSpacing(10)
        layout.addLayout(title_col)
        layout.addStretch()
        return panel

    def _build_input_panel(self):
        panel = QWidget()
        panel.setObjectName("input_panel")
        outer = QVBoxLayout(panel)
        outer.setSpacing(10)

        # Baris 1: URL
        url_row = QHBoxLayout()
        url_label = QLabel("URL Berita")
        url_label.setFixedWidth(90)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://contoh.com/berita  ← masukkan URL halaman berita")
        url_row.addWidget(url_label)
        url_row.addWidget(self.url_input)
        outer.addLayout(url_row)

        # Baris 2: Limit + Tanggal
        opt_row = QHBoxLayout()
        opt_row.setSpacing(16)

        lim_label = QLabel("Limit Artikel")
        lim_label.setFixedWidth(90)
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(1, 9999)
        self.limit_spin.setValue(20)
        self.limit_spin.setFixedWidth(80)

        from_label = QLabel("Start Date")
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        self.date_from.setFixedWidth(120)

        to_label = QLabel("End Date")
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setFixedWidth(120)

        opt_row.addWidget(lim_label)
        opt_row.addWidget(self.limit_spin)
        opt_row.addSpacing(20)
        opt_row.addWidget(from_label)
        opt_row.addWidget(self.date_from)
        opt_row.addWidget(to_label)
        opt_row.addWidget(self.date_to)
        opt_row.addStretch()
        outer.addLayout(opt_row)

        # Baris 3: Tombol
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.start_button = QPushButton("▶  Start Scraping")
        self.start_button.setObjectName("btn_start")
        self.start_button.setFixedHeight(38)
        self.start_button.clicked.connect(self.start_scraping)

        self.btn_stop = QPushButton("■  Stop")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setFixedHeight(38)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self._stop_scraping)

        self.btn_export = QPushButton("💾  Export CSV")
        self.btn_export.setObjectName("btn_export")
        self.btn_export.setFixedHeight(38)
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self._export_csv)

        btn_row.addWidget(self.start_button)
        btn_row.addWidget(self.btn_stop)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_export)
        outer.addLayout(btn_row)

        return panel

    def _build_progress_section(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        prog_label = QLabel("Progress:")
        prog_label.setFixedWidth(60)

        self.start_button = QPushButton("Start Scraping")
        self.export_button = QPushButton("Export CSV")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setFixedHeight(18)

        layout.addWidget(prog_label)
        layout.addWidget(self.progress_bar)
        return widget

    def _build_table_section(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["No", "Judul", "Tanggal", "Portal", "Editor", "Isi Singkat"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return self.table

    def _build_statusbar(self):
        self.status_label = QLabel("Siap. Masukkan URL dan klik Start Scraping.")
        self.status_label.setObjectName("status_label")
        return self.status_label

    def _set_scraping_state(self, running: bool):
        self.start_button.setEnabled(not running)
        self.btn_stop.setEnabled(running)
        self.url_input.setEnabled(not running)
        self.limit_spin.setEnabled(not running)
        self.date_from.setEnabled(not running)
        self.date_to.setEnabled(not running)

    def _stop_scraping(self):
        if self._thread and self._thread.isRunning():
            self._thread.terminate()
            self._thread.wait()
            self._set_scraping_state(False)
            self.status_label.setText("Scraping dihentikan oleh pengguna.")
            if self._articles:
                self.btn_export.setEnabled(True)

    def _export_csv(self):
        if not self._articles:
            QMessageBox.information(self, "Tidak Ada Data", "Belum ada artikel untuk di-export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan CSV", "hasil_scraping.csv", "CSV Files (*.csv)"
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "date", "content", "portal", "editor"])
                writer.writeheader()
                for art in self._articles:
                    row = dict(art)
                    if row.get("date") is not None:
                        row["date"] = row["date"].strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow(row)
            self.status_label.setText(f"Export berhasil: {path}")
            QMessageBox.information(self, "Export Berhasil", f"File disimpan di:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    # implementasi thread untuk menangani proses scraping agar GUI tetap responsif
    # fungsi untuk memulai proses scraping ketika tombol start ditekan
    def start_scraping(self):
        from datetime import datetime

        # pengambilan input url dan parameter limit, start_date, dan end_date dari GUI
        url = self.url_input.text().strip()
        limit = self.limit_spin.value()
        start_date = datetime.combine(self.date_from.date().toPyDate(), datetime.min.time())
        end_date = datetime.combine(self.date_to.date().toPyDate(), datetime.max.time())

        # validasi input
        if not url:
            QMessageBox.warning(self, "URL Kosong", "Masukkan URL berita terlebih dahulu!")
            return
        if not url.startswith("http"):
            QMessageBox.warning(self, "URL Tidak Valid", "URL harus diawali dengan http:// atau https://")
            return
        if limit < 1:
            QMessageBox.warning(self, "Limit Tidak Valid", "Limit harus ≥ 1.")
            return
        if start_date > end_date:
            QMessageBox.warning(self, "Rentang Tanggal Salah",
                                "Start Date tidak boleh lebih besar dari End Date.")
            return

        # reset UI
        self.table.setRowCount(0)
        self._articles = []
        self.progress_bar.setValue(0)
        self.btn_export.setEnabled(False)
        self._set_scraping_state(True)
        self.status_label.setText(f"Scraping dimulai: {url}")

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
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"Mengambil artikel... {progress}%")

    # menangani hasil scraping dari thread scraper (harusnya hasil di tabel)
    def show_results(self, data):
        self._articles = data
        self.table.setRowCount(0)

        for row_idx, art in enumerate(data):
            self.table.insertRow(row_idx)

            title   = art.get("title", "-")
            date    = art.get("date", None)
            content = art.get("content", "")
            portal  = art.get("portal", "-")
            editor  = art.get("editor", "-")

            date_str = date.strftime("%d-%m-%Y") if date else "N/A"
            preview  = content[:150] + "..." if len(content) > 150 else content

            no_item = QTableWidgetItem(str(row_idx + 1))
            no_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 0, no_item)
            self.table.setItem(row_idx, 1, QTableWidgetItem(title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(date_str))
            self.table.setItem(row_idx, 3, QTableWidgetItem(portal))
            self.table.setItem(row_idx, 4, QTableWidgetItem(editor))
            self.table.setItem(row_idx, 5, QTableWidgetItem(preview))

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
