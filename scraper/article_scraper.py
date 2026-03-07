import time
import dateutil.parser
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_articles(url, driver):
    # log terminal buat mantau proses
    print(f"   > [{time.strftime('%H:%M:%S')}] Scrappingcls data dari: {url}")
    
    try:
        driver.get(url)
        time.sleep(2) # kasih nafas buat load konten

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Ambil Judul
        title = soup.title.string if soup.title else ""
        h1 = soup.find('h1')
        if h1 and len(h1.text) > 10:
            title = h1.text.strip()
            
        if not title or len(title) < 5:
            return None 
            
        # 2. Ambil Tanggal
        # nyari di meta tag atau tag time yang umum di portal berita
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
                date_obj = dateutil.parser.parse(date_str).date()
            except:
                date_obj = datetime.now().date()
        else:
            date_obj = datetime.now().date()
            
        # 3. Portal & 4. Editor
        portal = url.split('/')[2].replace('www.', '')
        editor = "Anonym"
        author_meta = soup.find('meta', attrs={'name': 'author'}) or \
                      soup.find('meta', property='article:author')
        if author_meta and author_meta.get('content'):
            editor = author_meta['content']
                
        # 5. Ambil Isi Artikel
        content_paragraphs = []
        # asumsi container body pake tag article atau div detail
        article_body = soup.find('article') or soup.find('div', class_=lambda c: c and 'detail' in c.lower()) or soup.body
        
        if article_body:
            for p in article_body.find_all('p'):
                text = p.text.strip()
                # filter paragraf pendek atau iklan 'baca juga'
                if len(text) > 30 and "baca juga" not in text.lower():
                    content_paragraphs.append(text)
                    
        content = "\n\n".join(content_paragraphs)
        if len(content) < 100: # anggap bukan artikel kalau terlalu pendek
            return None 

        return {
            "title": title,
            "date": date_obj,
            "portal": portal,
            "editor": editor,
            "content": content
        }

    except Exception as e:
        print(f"      [!] Skip link: {e}")
        return None