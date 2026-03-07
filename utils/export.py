import csv
from PyQt5.QtWidgets import QFileDialog
def export_to_csv(self):
    path, _ = QFileDialog.getSaveFileName(
        self,
        "Save File",
        "",
        "CSV Files (*.csv)"
    )

    if not path:
        return

    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # ambil header tabel
        headers = []
        for col in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(col).text())
        writer.writerow(headers)

        # ambil isi tabel
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            writer.writerow(row_data)
