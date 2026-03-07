import time
from datetime import datetime
import dateutil.parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_articles(url):
    print(f"[{time.strftime('%H:%M:%S')}] Menggores data dari: {url}")
    
    # Konfigurasi Headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    article_data = None
    
    try:
        driver.get(url)
        time.sleep(2) # memberinya waktu untuk memuat aset statis dasar

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Scraping Judul
        title = soup.title.string if soup.title else ""
        h1 = soup.find('h1')
        if h1 and len(h1.text) > 10:
            title = h1.text.strip()
            
        if not title:
            return None # Skip jika tanpa judul
            
        # 2. Scraping Tanggal
        # Mencoba mencari format tanggal umum di meta tag atau div class bertema date/time
        date_obj = None
        date_str = ""
        meta_date = soup.find('meta', property='article:published_time') or \
                    soup.find('meta', itemprop='datePublished')
        
        if meta_date and meta_date.get('content'):
            date_str = meta_date['content']
        else:
            time_tag = soup.find('time')
            if time_tag:
                date_str = time_tag.get('datetime', time_tag.text)
                
        if date_str:
            try:
                date_obj = dateutil.parser.parse(date_str).date() # ambil tanggal (tanpa timezone utk komparasi aman)
            except:
                date_obj = datetime.now().date()
        else:
            date_obj = datetime.now().date()
            
        # 3. Scraping Portal Berita (dari domain atau meta tag nama site)
        portal = "Akses Website"
        meta_site = soup.find('meta', property='og:site_name')
        if meta_site and meta_site.get('content'):
            portal = meta_site['content']
        else:
            portal = url.split('/')[2].replace('www.', '')

        # 4. Scraping Editor / Author
        editor = "Anonym"
        author_meta = soup.find('meta', attrs={'name': 'author'}) or \
                      soup.find('meta', property='article:author')
        if author_meta and author_meta.get('content'):
            editor = author_meta['content']
        else:
            # tebak kelas author/editor yang paling umum pada markup
            author_div = soup.find(lambda tag: tag.name in ['div', 'span', 'a'] and tag.get('class') and any('author' in c.lower() or 'editor' in c.lower() for c in tag.get('class')))
            if author_div:
                editor = author_div.text.strip()
                
        # 5. Scraping Content (Isi Artikel)
        content_paragraphs = []
        # Beberapa asumsi struktur konten di tag p dalam container utama
        article_body = soup.find('article') or soup.find('div', class_=lambda c: c and 'detail' in c.lower()) or soup.body
        
        if article_body:
            for p in article_body.find_all('p'):
                text = p.text.strip()
                # filter paragraf kosong atau iklan pendek
                if len(text) > 20 and "baca juga" not in text.lower():
                    content_paragraphs.append(text)
                    
        content = "\n\n".join(content_paragraphs)
        if not content:
            return None # Skip jika tubuh konten kosong

        article_data = {
            "title": title,
            "date": date_obj, # Format objek datetime.date
            "portal": portal,
            "editor": editor,
            "content": content
        }

    except Exception as e:
        print(f"Error scraping artikel {url}: {e}")
    finally:
        driver.quit()
        
    return article_data

