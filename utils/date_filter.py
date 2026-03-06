# TODO: implement filter_by_date()
from datetime import datetime

def filter_by_date(data, start_date, end_date):
    # implementasi fungsi untuk memfilter artikel berdasarkan tanggal
    # menerima input berupa list data artikel
    # setiap artikel memiliki field tanggal
    # filter artikel yang berada di antara start_date dan end_date
    # kembalikan list artikel yang sesuai dengan rentang tanggal
    
    # dummy data untuk testing
    filtered_data = []
    for item in data:
        article_date = datetime.strptime(item['date'], "%Y-%m-%d")
        if start_date <= article_date <= end_date:
            filtered_data.append(item)
    return filtered_data