import requests
import pymysql
import time
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'shinzan202',
    'database': 'sakurasou',
    'charset': 'utf8mb4'
}

JIKAN_API = 'https://api.jikan.moe/v4'

CATEGORY_MAP = {
    'Action': '热血', 'Adventure': '冒险', 'Comedy': '搞笑',
    'Drama': '剧情', 'Fantasy': '奇幻', 'Horror': '悬疑',
    'Mystery': '悬疑', 'Romance': '恋爱', 'Sci-Fi': '科幻',
    'Slice of Life': '日常', 'Sports': '运动', 'Supernatural': '奇幻',
    'School': '校园', 'Music': '音乐', 'Mecha': '机战',
    'Seinen': '热血', 'Shounen': '热血', 'Shoujo': '恋爱',
    'Josei': '日常', 'Harem': '后宫', 'Thriller': '悬疑',
    'Military': '冒险', 'Space': '科幻', 'Police': '悬疑'
}

TYPE_MAP = {'tv': 'tv', 'movie': 'movie', 'ova': 'ova', 'ona': 'ona', 'special': 'special'}

def get_db():
    return pymysql.connect(**DB_CONFIG)

def get_category_id(name, cursor):
    cursor.execute('SELECT id FROM categories WHERE slug = %s', (name.lower(),))
    row = cursor.fetchone()
    return row[0] if row else None

def fetch_anime_top(page=1):
    url = f'{JIKAN_API}/top/anime?page={page}&limit=25&filter=bypopularity'
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            print(f'[Jikan] HTTP {resp.status_code}')
            return []
        data = resp.json()
        items = []
        for a in data.get('data', []):
            titles = a.get('titles', [])
            title_en = ''
            title_jp = ''
            for t in titles:
                if t.get('type') == 'Default':
                    title_en = t.get('title', '')
                if t.get('type') == 'Japanese':
                    title_jp = t.get('title', '')

            genres = [g['name'] for g in a.get('genres', [])]
            status = a.get('status', '')
            status_map = {
                'Currently Airing': 'ongoing',
                'Finished Airing': 'completed',
                'Not yet aired': 'upcoming'
            }

            items.append({
                'title': title_en or title_jp or a.get('title', ''),
                'alias': title_jp if title_jp and title_en else '',
                'cover': a.get('images', {}).get('jpg', {}).get('large_image_url', ''),
                'description': (a.get('synopsis') or '')[:500],
                'rating': float(a.get('score', 0) or 0),
                'year': a.get('year', 0) or 0,
                'status': status_map.get(status, 'ongoing'),
                'type': TYPE_MAP.get(a.get('type', ''), 'tv'),
                'episodes_total': a.get('episodes', 0) or 0,
                'categories': genres,
                'mal_id': a.get('mal_id', 0)
            })
        print(f'[Jikan] Page {page}: got {len(items)} animes')
        return items
    except Exception as e:
        print(f'[Jikan] Error: {e}')
        return []

def fetch_anime_seasonal(year=2026, season='spring'):
    url = f'{JIKAN_API}/seasons/{year}/{season}?limit=25'
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
        items = []
        for a in data.get('data', []):
            titles = a.get('titles', [])
            title_en = ''
            title_jp = ''
            for t in titles:
                if t.get('type') == 'Default':
                    title_en = t.get('title', '')
                if t.get('type') == 'Japanese':
                    title_jp = t.get('title', '')

            genres = [g['name'] for g in a.get('genres', [])]
            status = a.get('status', '')
            status_map = {
                'Currently Airing': 'ongoing',
                'Finished Airing': 'completed',
                'Not yet aired': 'upcoming'
            }

            items.append({
                'title': title_en or title_jp or a.get('title', ''),
                'alias': title_jp if title_jp and title_en else '',
                'cover': a.get('images', {}).get('jpg', {}).get('large_image_url', ''),
                'description': (a.get('synopsis') or '')[:500],
                'rating': float(a.get('score', 0) or 0),
                'year': a.get('year', year),
                'status': status_map.get(status, 'ongoing'),
                'type': TYPE_MAP.get(a.get('type', ''), 'tv'),
                'episodes_total': a.get('episodes', 0) or 0,
                'categories': genres,
                'mal_id': a.get('mal_id', 0)
            })
        print(f'[Jikan Seasonal] {year} {season}: got {len(items)} animes')
        return items
    except Exception as e:
        print(f'[Jikan Seasonal] Error: {e}')
        return []

def save_anime(anime_data, cursor, db):
    cursor.execute('SELECT id FROM animes WHERE title = %s', (anime_data['title'],))
    existing = cursor.fetchone()
    if existing:
        return existing[0]

    # Generate episodes for some animes
    ep_count = anime_data.get('episodes_total', 0)
    if ep_count <= 0:
        ep_count = 12

    # Create demo episode URLs using embed
    ep_list = []
    for i in range(1, min(ep_count + 1, 24)):
        ep_list.append({
            'number': i,
            'title': f'第{i}集' if i > 1 else '第1集',
            'video_url': ''
        })

    sql = '''INSERT INTO animes (title, alias, cover, description, rating, year, status, region, type, episodes_total, views)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(sql, (
        anime_data['title'],
        anime_data.get('alias', ''),
        anime_data.get('cover', ''),
        anime_data.get('description', '') or '暂无简介',
        anime_data.get('rating', 0),
        anime_data.get('year', 0) or 0,
        anime_data.get('status', 'ongoing'),
        '日本',
        anime_data.get('type', 'tv'),
        len(ep_list),
        max(1000, int(anime_data.get('rating', 0) * 10000))
    ))
    anime_id = cursor.lastrowid

    for cat_name in anime_data.get('categories', []):
        cn_name = CATEGORY_MAP.get(cat_name, cat_name)
        cursor.execute('SELECT id FROM categories WHERE name = %s', (cn_name,))
        cat_row = cursor.fetchone()
        if cat_row:
            try:
                cursor.execute(
                    'INSERT IGNORE INTO anime_categories (anime_id, category_id) VALUES (%s, %s)',
                    (anime_id, cat_row[0])
                )
            except:
                pass

    for ep in ep_list:
        try:
            cursor.execute(
                'INSERT INTO episodes (anime_id, number, title, video_url, duration, views) VALUES (%s, %s, %s, %s, %s, %s)',
                (anime_id, ep['number'], ep['title'], ep['video_url'], 24, max(100, int(anime_data.get('rating', 0) * 500)))
            )
        except:
            pass

    db.commit()
    print(f'  [OK] {anime_data["title"]} (ID: {anime_id}, eps: {len(ep_list)})')
    return anime_id

def run(pages=5):
    db = get_db()
    cursor = db.cursor()
    total = 0

    print('=' * 50)
    print('[Jikan] Fetching popular anime...')
    print('=' * 50)
    for p in range(1, pages + 1):
        items = fetch_anime_top(p)
        if not items:
            break
        for item in items:
            try:
                save_anime(item, cursor, db)
                total += 1
                time.sleep(0.5)
            except Exception as e:
                print(f'  [ERR] {item.get("title", "?")}: {e}')
                db.rollback()
        time.sleep(1)

    print(f'\n{"="*50}')
    print(f'[DONE] Total saved: {total} animes')
    print(f'{"="*50}')

    cursor.close()
    db.close()

if __name__ == '__main__':
    pages = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    run(pages)
