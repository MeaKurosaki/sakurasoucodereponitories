import requests
from bs4 import BeautifulSoup
import re
import time
import pymysql
import json
from urllib.parse import urljoin
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'shinzan202',
    'database': 'sakurasou',
    'charset': 'utf8mb4'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Referer': 'https://www.bing.com/'
}

SOURCES = [
    {
        'name': 'agefans',
        'base_url': 'https://www.agefans.cc',
        'enabled': True
    },
    {
        'name': 'yinghuacd',
        'base_url': 'https://www.yinghuacd.com',
        'enabled': True
    }
]

def get_db():
    return pymysql.connect(**DB_CONFIG)

def get_category_id(name, cursor):
    slug_map = {
        '热血': 'action', '恋爱': 'romance', '搞笑': 'comedy',
        '奇幻': 'fantasy', '科幻': 'sci-fi', '悬疑': 'mystery',
        '日常': 'slice-of-life', '校园': 'school', '冒险': 'adventure',
        '后宫': 'harem', '百合': 'yuri', '耽美': 'yaoi',
        '机战': 'mecha', '运动': 'sports', '音乐': 'music',
        '战斗': 'action', '爱情': 'romance', '喜剧': 'comedy',
        '魔法': 'fantasy', '穿越': 'fantasy', '异世界': 'fantasy'
    }
    slug = slug_map.get(name, name.lower().replace(' ', '-'))
    cursor.execute('SELECT id FROM categories WHERE slug = %s', (slug,))
    row = cursor.fetchone()
    return row[0] if row else None

def scrape_agefans(page=1):
    """Scrape anime list from agefans"""
    url = f'https://www.agefans.cc/catalog/all-all-all-all-all-time-{page}.json'
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f'[agefans] Failed to fetch page {page}: {resp.status_code}')
            return []
        data = resp.json()
        items = []
        for item in data.get('catalog', []):
            items.append({
                'title': item.get('name', ''),
                'alias': item.get('alias', '') or '',
                'cover': item.get('cover', '') or '',
                'description': item.get('description', '') or '',
                'rating': float(item.get('score', 0) or 0),
                'year': item.get('year', 0) or 0,
                'status': item.get('status', 0),
                'type': item.get('type', 0),
                'region': item.get('region', '') or '未知',
                'episodes_total': item.get('episodes_count', 0) or 0,
                'categories': [c.get('tag_name', '') for c in item.get('tags', [])]
            })
        print(f'[agefans] Fetched {len(items)} items from page {page}')
        return items
    except Exception as e:
        print(f'[agefans] Error: {e}')
        return []

def scrape_yinghuacd(page=1):
    """Scrape anime list from yinghuacd"""
    url = f'https://www.yinghuacd.com/list/page/{page}.html'
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        if resp.status_code != 200:
            print(f'[yinghuacd] Failed to fetch page {page}')
            return []
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = []
        cards = soup.select('.card-item, .module-item, .video-card')
        for card in cards:
            title_el = card.select_one('.card-title a, .module-title a, a')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            link = title_el.get('href', '')
            cover_el = card.select_one('img')
            cover = cover_el.get('data-src') or cover_el.get('src', '') if cover_el else ''
            if not title:
                continue
            items.append({
                'title': title,
                'alias': '',
                'cover': urljoin(url, cover) if cover else '',
                'description': '',
                'rating': 0.0,
                'year': 0,
                'status': 'ongoing',
                'type': 'tv',
                'region': '日本',
                'episodes_total': 0,
                'categories': [],
                'detail_url': urljoin(url, link) if link else ''
            })
        print(f'[yinghuacd] Fetched {len(items)} items from page {page}')
        return items
    except Exception as e:
        print(f'[yinghuacd] Error: {e}')
        return []

def save_anime(anime_data, cursor, db):
    """Save anime to database"""
    status_map = {0: 'ongoing', 1: 'completed', 2: 'upcoming'}
    type_map = {0: 'tv', 1: 'movie', 2: 'ova', 3: 'ona', 4: 'special'}

    cursor.execute(
        'SELECT id FROM animes WHERE title = %s',
        (anime_data['title'],)
    )
    existing = cursor.fetchone()
    if existing:
        return existing[0]

    status = anime_data.get('status', 'ongoing')
    if isinstance(status, int):
        status = status_map.get(status, 'ongoing')
    anime_type = anime_data.get('type', 'tv')
    if isinstance(anime_type, int):
        anime_type = type_map.get(anime_type, 'tv')

    sql = '''INSERT INTO animes (title, alias, cover, description, rating, year, status, region, type, episodes_total)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(sql, (
        anime_data['title'],
        anime_data.get('alias', '') or '',
        anime_data.get('cover', '') or '',
        anime_data.get('description', '') or '',
        anime_data.get('rating', 0) or 0,
        anime_data.get('year', 0) or 0,
        status,
        anime_data.get('region', '日本') or '日本',
        anime_type,
        anime_data.get('episodes_total', 0) or 0
    ))
    db.commit()
    anime_id = cursor.lastrowid

    for cat_name in anime_data.get('categories', []):
        cat_id = get_category_id(cat_name, cursor)
        if cat_id:
            try:
                cursor.execute(
                    'INSERT IGNORE INTO anime_categories (anime_id, category_id) VALUES (%s, %s)',
                    (anime_id, cat_id)
                )
            except:
                pass
    db.commit()
    print(f'  [OK] Saved: {anime_data["title"]} (ID: {anime_id})')
    return anime_id

def run_scraper(source_name=None, pages=3):
    """Run scraper for specified source(s)"""
    db = get_db()
    cursor = db.cursor()
    total = 0

    sources = [s for s in SOURCES if s.get('enabled')]
    if source_name:
        sources = [s for s in sources if s['name'] == source_name]

    scrapers = {
        'agefans': scrape_agefans,
        'yinghuacd': scrape_yinghuacd
    }

    for source in sources:
        name = source['name']
        if name not in scrapers:
            continue
        print(f'\n{"="*50}')
        print(f'[Scraping] {name} ({source["base_url"]})')
        print(f'{"="*50}')
        for p in range(1, pages + 1):
            items = scrapers[name](p)
            if not items:
                print(f'  No items found on page {p}, stopping.')
                break
            for item in items:
                try:
                    save_anime(item, cursor, db)
                    total += 1
                    time.sleep(0.3)
                except Exception as e:
                    print(f'  [ERR] Error saving {item.get("title", "?")}: {e}')
                    db.rollback()
            time.sleep(1)

    cursor.close()
    db.close()
    print(f'\n{"="*50}')
    print(f'[DONE] Total saved: {total} animes')
    print(f'{"="*50}')

if __name__ == '__main__':
    source = sys.argv[1] if len(sys.argv) > 1 else None
    pages = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    run_scraper(source, pages)
