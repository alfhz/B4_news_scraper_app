from datetime import datetime

def filter_by_date(data, start_date, end_date):
    filtered_data = []
    for art in data:
        art_date = art.get("date")
        
        if art_date:
            # pastikan semuanya bertipe date untuk perbandingan yang aman
            s_date = start_date.date() if hasattr(start_date, 'date') else start_date
            e_date = end_date.date() if hasattr(end_date, 'date') else end_date
            a_date = art_date.date() if hasattr(art_date, 'date') else art_date
            
            if s_date <= a_date <= e_date:
                filtered_data.append(art)
        else:
            filtered_data.append(art)
    return filtered_data
