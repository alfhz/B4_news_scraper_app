from datetime import datetime
def filter_by_date(self, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    for row in range(self.table.rowCount()):
        item = self.table.item(row, 1)  # kolom tanggal (misalnya kolom ke-2)
        
        if item is None:
            continue

        tanggal = datetime.strptime(item.text(), "%Y-%m-%d")

        if start <= tanggal <= end:
            self.table.setRowHidden(row, False)
        else:
            self.table.setRowHidden(row, True)
