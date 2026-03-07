from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
<<<<<<< Updated upstream
from urllib.parse import urlparse, urljoin
=======
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
>>>>>>> Stashed changes
import time


def get_article_links(url, limit):
<<<<<<< Updated upstream
    """
    Mengambil semua link artikel dari halaman berita (homepage/kategori).
    Mendukung pagination otomatis dan limit jumlah link.

    Parameters:
        url   (str): URL halaman berita utama / kategori.
        limit (int): Batas maksimal jumlah link yang dikumpulkan.

    Returns:
        list[str]: Daftar URL artikel unik, maksimal sejumlah limit.
    """
    driver = None
    collected_links = []
    visited_pages = set()

    try:
        # Setup headless Chrome
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)

        # Ambil domain asal untuk filter link
        base_domain = _get_base_domain(url)
        current_url = url

        # Batas maksimum halaman pagination untuk menghindari infinite loop
        max_pages = 50
        page_count = 0

        while current_url and page_count < max_pages:
            # Cek apakah halaman sudah pernah dikunjungi (hindari infinite loop)
            if current_url in visited_pages:
                print(f"[link_collector] Halaman sudah dikunjungi, berhenti: {current_url}")
                break
            visited_pages.add(current_url)
            page_count += 1

            print(f"[link_collector] Scraping halaman {page_count}: {current_url}")

            try:
                driver.get(current_url)
                time.sleep(2)  # Tunggu halaman render
            except Exception as e:
                print(f"[link_collector] Error loading page {current_url}: {e}")
                break

            # Ambil semua link dari halaman saat ini
            new_links = _extract_article_links(driver, base_domain, url)
            print(f"[link_collector] Ditemukan {len(new_links)} link di halaman {page_count}")

            # Tambahkan link unik ke koleksi
            for link in new_links:
                if link not in collected_links:
                    collected_links.append(link)

                # Stop jika sudah mencapai limit
                if len(collected_links) >= limit:
                    break

            # Stop jika sudah mencapai limit
            if len(collected_links) >= limit:
                print(f"[link_collector] Limit {limit} tercapai, berhenti.")
                break

            # Cari tombol next / halaman berikutnya
            next_url = _find_next_page(driver, current_url)
            if not next_url or next_url == current_url:
                print("[link_collector] Tidak ada halaman berikutnya, berhenti.")
                break  # Tidak ada halaman berikutnya

            current_url = next_url

            # Delay antar halaman agar tidak membebani server
            time.sleep(1)

        print(f"[link_collector] Total link terkumpul: {len(collected_links[:limit])}")
        return collected_links[:limit]

    except Exception as e:
        print(f"[link_collector] Error: {e}")
        return collected_links[:limit]

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


# ============================================================
#  HELPER FUNCTIONS
# ============================================================

def _get_base_domain(url):
    """
    Ambil domain dasar dari URL.
    Contoh: "https://news.detik.com/kategori" → "detik.com"
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        # Ambil 2 level terakhir untuk base domain (misal: detik.com dari news.detik.com)
        parts = domain.split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return domain
    except Exception:
        return ""


def _extract_article_links(driver, base_domain, source_url):
    """
    Ekstrak semua link artikel dari halaman yang sedang terbuka.
    Filter hanya link yang kemungkinan besar adalah artikel berita.

    Strategy:
    1. Ambil semua <a> tag yang memiliki href
    2. Filter berdasarkan domain (harus sama dengan base_domain)
    3. Filter berdasarkan pola URL artikel (mengandung path yang cukup panjang)
    4. Buang link navigasi, media sosial, category, tag, author, dll.
    """
    links = []

    try:
        all_anchors = driver.find_elements(By.TAG_NAME, "a")

        for anchor in all_anchors:
            try:
                href = anchor.get_attribute("href")
                if not href:
                    continue

                # Normalisasi URL relatif ke absolut
                href = urljoin(source_url, href)

                # Pastikan URL valid dan memiliki skema HTTP(S)
                parsed = urlparse(href)
                if parsed.scheme not in ("http", "https"):
                    continue

                # Filter: harus dari domain yang sama
                link_domain = parsed.netloc
                if link_domain.startswith("www."):
                    link_domain = link_domain[4:]
                # Cek apakah base domain ada di link domain
                if base_domain not in link_domain:
                    continue

                # Filter: buang link non-artikel
                if _is_non_article_link(href, source_url):
                    continue

                # Filter: URL artikel biasanya punya path yang cukup panjang
                path = parsed.path.strip("/")
                if not path or len(path) < 5:
                    continue

                # Buang duplikat dengan menghapus fragment dan trailing slash
                clean_url = parsed.scheme + "://" + parsed.netloc + parsed.path
                if clean_url.endswith("/"):
                    clean_url = clean_url[:-1]

                if clean_url not in links:
                    links.append(clean_url)

            except Exception:
                continue

    except Exception as e:
        print(f"[link_collector] Error extracting links: {e}")

    return links


def _is_non_article_link(url, source_url):
    """
    Cek apakah URL kemungkinan bukan artikel berita melainkan
    halaman navigasi/kategori/dll.
    Return True jika URL harus DIBUANG.
    """
    url_lower = url.lower()
    parsed = urlparse(url_lower)
    path = parsed.path

    # Buang jika URL sama dengan halaman sumber
    if url.rstrip("/") == source_url.rstrip("/"):
        return True

    # Pattern URL non-artikel
    non_article_patterns = [
        "/tag/", "/tags/", "/kategori/", "/category/", "/categories/",
        "/author/", "/penulis/", "/editor/",
        "/page/", "/search", "/login", "/register", "/signup",
        "/about", "/contact", "/privacy", "/terms",
        "/foto/", "/galeri/", "/gallery/", "/photo/",
        "/video/", "/videos/",
        "/indeks", "/index/",
        "/topik/", "/topic/",
        "/admin", "/wp-admin", "/wp-login",
    ]
    for pattern in non_article_patterns:
        if pattern in path:
            return True

    # Buang link ke halaman utama / homepage
    if path in ("", "/", "/index.html", "/index.php"):
        return True

    # Buang link media sosial, share, dll.
    social_domains = [
        "facebook.com", "twitter.com", "instagram.com", "youtube.com",
        "tiktok.com", "wa.me", "whatsapp.com", "t.me", "telegram",
        "linkedin.com", "pinterest.com",
    ]
    for social in social_domains:
        if social in url_lower:
            return True

    # Buang link file langsung (gambar, pdf, dll)
    file_extensions = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".mp4", ".mp3"]
    for ext in file_extensions:
        if path.endswith(ext):
            return True

    return False


def _find_next_page(driver, current_url):
    """
    Cari link ke halaman berikutnya (pagination).
    Fallback bertingkat:
    1. <a rel="next">
    2. Link/button dengan text "Next", "Selanjutnya", "›", "»", dsb.
    3. Link pagination dengan CSS selector umum

    Return URL halaman berikutnya atau None.
    """
    # Prioritas 1: <a rel="next">
    try:
        next_link = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
        href = next_link.get_attribute("href")
        if href:
            return urljoin(current_url, href)
    except Exception:
        pass

    # Prioritas 2: Link/button dengan teks umum untuk "next"
    next_text_patterns = [
        "next", "selanjutnya", "berikutnya", "lanjut",
        "›", "»", "→", ">>", ">",
        "next page", "halaman berikutnya",
    ]

    try:
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            try:
                text = link.text.strip().lower()
                # Cek juga aria-label
                aria_label = (link.get_attribute("aria-label") or "").strip().lower()

                for pattern in next_text_patterns:
                    if text == pattern or aria_label == pattern:
                        href = link.get_attribute("href")
                        if href and href != current_url:
                            return urljoin(current_url, href)
            except Exception:
                continue
    except Exception:
        pass

    # Prioritas 3: CSS selectors umum untuk pagination next
    pagination_selectors = [
        '.pagination a.next',
        '.pagination .next a',
        '.paging a.next',
        '.page-nav a.next',
        'a.page-next',
        'nav.pagination a:last-child',
        '.nav-links a.next',
        'a[class*="next"]',
        'li[class*="next"] a',
    ]
    for selector in pagination_selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, selector)
            href = el.get_attribute("href")
            if href and href != current_url:
                return urljoin(current_url, href)
        except Exception:
            continue

    return None
=======
    print(f"[{time.strftime('%H:%M:%S')}] Mengumpulkan link dari: {url} (Limit: {limit})")
    
    # Konfigurasi Headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Gunakan User-Agent asli agar tidak diblokir
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    collected_links = set()
    
    try:
        driver.get(url)
        time.sleep(2)  # Tunggu page load awal

        scroll_attempts = 0
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(collected_links) < limit and scroll_attempts < 10:
            # Ambil semua link menggunakan JavaScript agar jauh lebih cepat (tidak membuat aplikasi hang)
            hrefs = driver.execute_script("return Array.from(document.querySelectorAll('a')).map(a => a.href);")
            for href in hrefs:
                # Filter kasar untuk memastikan ini link dari situs berita
                if href and href.startswith("http") and ("/" in href.replace("https://", "").replace("http://", "")):
                    # Hindari link ke home, kategori utama / tag saja
                    if len(href.split('/')) > 4: 
                        collected_links.add(href)
                        if len(collected_links) >= limit:
                            break
                            
            if len(collected_links) >= limit:
                break
            
            # Scroll ke bawah untuk mencoba lazy-load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_height = new_height

    except Exception as e:
        print(f"Error saat mengumpulkan link: {e}")
    finally:
        driver.quit()
        
    result_list = list(collected_links)[:limit]
    print(f"[{time.strftime('%H:%M:%S')}] Ditemukan {len(result_list)} link target.")
    return result_list
>>>>>>> Stashed changes
