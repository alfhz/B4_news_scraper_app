from datetime import datetime
def filter_by_date(data_list, start, end):
    filtered_data = []

    for article in data_list:
        tanggal = article.get("date")  # kolom tanggal (misalnya kolom ke-2)
        
        if tanggal is None:
            filtered_data.append(article)
            continue
        
        if isinstance(tanggal, datetime):
            if start <= tanggal <= end:
                filtered_data.append(article)
        else:
            filtered_data.append(article)
            
    return filtered_data

