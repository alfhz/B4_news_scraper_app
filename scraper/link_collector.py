from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin
import time


def get_article_links(url, limit):
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