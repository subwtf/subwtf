import json
import urllib.request
import urllib.parse
import re
import os

REFRAL_LINK = "https://iseetv.net/welcome/signup/cb26f9e15332cb38"

CATEGORIES = [
    "IPTV Плееры", "Медиацентры", "Smart TV", "Кино и Сериалы", 
    "Видеоплееры", "Аудио и Радио", "Утилиты TV", "Файловые менеджеры",
    "Браузеры", "Лаунчеры", "Оптимизация", "Безопасность", 
    "Тесты скорости", "Управление ДУ", "Инструменты", "Системные",
    "Игровые эмуляторы", "Другое"
]

# Базовая элитная подборка
APPS_DATA = [
    {
        "slug": "televizo",
        "name": "Televizo",
        "category": "IPTV Плееры",
        "rating": "4.9",
        "icon": "📺",
        "fallback_apk": "https://televizo.net/apk/televizo.apk",
        "desc": "Современный и мощный IPTV плеер для Android TV и смартфонов. Поддержка M3U и Xtream Codes."
    },
    {
        "slug": "smarttube",
        "name": "SmartTube",
        "category": "Smart TV",
        "rating": "5.0",
        "icon": "🔴",
        "fallback_apk": "https://github.com/yuliskov/SmartTube/releases",
        "desc": "Продвинутый клиент YouTube для Android TV и приставок с автопропуском интеграций и без рекламы."
    }
]

def aggressive_github_parser():
    """Жесткий парсер GitHub без разбора на закрытость/открытость"""
    queries = ["android apk release", "smarttv apk", "iptv player apk", "tools apk repository"]
    scraped = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    for q in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=15"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read().decode())
                for item in data.get('items', []):
                    name = item.get('name')
                    html_url = item.get('html_url')
                    desc = item.get('description') or "Автоматически извлеченный APK с репозитория."
                    
                    slug = re.sub(r'[^a-zA-Z0-9]', '-', name).lower().strip('-')
                    if not slug or any(a['slug'] == slug for a in APPS_DATA + scraped):
                        continue
                    
                    # Категоризация на лету
                    cat = "Другое"
                    txt = (name + " " + desc).lower()
                    if "iptv" in txt or "player" in txt: cat = "IPTV Плееры"
                    elif "media" in txt or "kodi" in txt: cat = "Медиацентры"
                    elif "tv" in txt or "remote" in txt: cat = "Smart TV"
                    elif "launcher" in txt: cat = "Лаунчеры"
                    elif "tool" in txt: cat = "Утилиты TV"

                    scraped.append({
                        "slug": slug,
                        "name": name,
                        "category": cat,
                        "rating": "4.8",
                        "icon": "⚡",
                        "fallback_apk": f"{html_url}/releases",
                        "desc": desc[:130] + "..."
                    })
        except Exception as e:
            print(f"Парсер пробил защиту, но поймал ошибку (не критично): {e}")
            
    return scraped

ALL_APPS = APPS_DATA + aggressive_github_parser()

HTML_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git App WTF 🤨 — Безжалостный парсер APK</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #090d16; color: #f1f5f9; line-height: 1.5; min-height: 100vh; }
        a { color: inherit; text-decoration: none; }
        .header { position: sticky; top: 0; z-index: 50; background: rgba(9, 13, 22, 0.9); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.08); padding: 1rem 1.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
        .logo { display: flex; align-items: center; gap: 0.75rem; font-weight: 800; font-size: 1.25rem; }
        .logo-box { width: 2.4rem; height: 2.4rem; border-radius: 0.75rem; background: linear-gradient(135deg, #f43f5e, #6366f1); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
        .search-container { flex-grow: 1; max-width: 350px; }
        .search-input { width: 100%; padding: 0.6rem 1rem; border-radius: 0.75rem; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); color: #fff; font-size: 0.875rem; outline: none; }
        .burger-btn { background: rgba(30,41,59,0.8); border: 1px solid rgba(255,255,255,0.1); color: #fff; padding: 0.5rem 0.75rem; border-radius: 0.55rem; cursor: pointer; font-size: 1.2rem; }
        
        .drawer { position: fixed; top: 0; right: -300px; width: 300px; height: 100vh; background: #0f172a; border-left: 1px solid rgba(255,255,255,0.08); z-index: 100; transition: right 0.3s ease; padding: 1.5rem; overflow-y: auto; }
        .drawer.open { right: 0; }
        .drawer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; font-weight: 800; font-size: 1.1rem; }
        .close-btn { background: none; border: none; color: #94a3b8; font-size: 1.5rem; cursor: pointer; }
        .drawer-item { display: block; padding: 0.6rem 0.8rem; border-radius: 0.5rem; color: #94a3b8; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem; transition: all 0.2s; }
        .drawer-item:hover { background: rgba(99,102,241,0.15); color: #818cf8; }

        .promo-card { background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(30, 41, 59, 0.8)); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 1.25rem; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 1rem; justify-content: space-between; }
        @media (min-width: 768px) { .promo-card { flex-direction: row; align-items: center; } }
        .promo-title { font-size: 1.15rem; font-weight: 800; color: #f8fafc; }
        .promo-sub { font-size: 0.85rem; color: #94a3b8; }
        .promo-btn { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; padding: 0.75rem 1.5rem; border-radius: 0.75rem; font-weight: 700; font-size: 0.875rem; white-space: nowrap; text-align: center; }
        
        .container { max-width: 1100px; margin: 0 auto; padding: 1rem 1.25rem 4rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }
        .app-card { background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 1.25rem; padding: 1.25rem; display: flex; gap: 1rem; transition: all 0.2s; }
        .app-card:hover { background: rgba(30, 41, 59, 0.8); border-color: rgba(99, 102, 241, 0.4); transform: translateY(-3px); }
        .app-icon { width: 3.5rem; height: 3.5rem; border-radius: 1rem; background: #020617; border: 1px solid rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; font-size: 1.75rem; flex-shrink: 0; }
        .app-body { flex-grow: 1; min-width: 0; }
        .app-title { font-size: 1rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.2rem; }
        .app-category { font-size: 0.75rem; color: #64748b; font-weight: 600; margin-bottom: 0.4rem; }
        .app-desc { font-size: 0.8rem; color: #94a3b8; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .footer { border-top: 1px solid rgba(255, 255, 255, 0.08); padding: 2.5rem 1.25rem; text-align: center; color: #64748b; font-size: 0.85rem; }
    </style>
</head>
<body>
    <header class="header">
        <a href="index.html" class="logo">
            <div class="logo-box">🤨</div>
            <div>Git App <span style="color:#f43f5e">WTF</span></div>
        </a>
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="Поиск по выкопанным APK...">
        </div>
        <button class="burger-btn" onclick="toggleDrawer()">☰ Категории</button>
    </header>

    <div class="drawer" id="catDrawer">
        <div class="drawer-header">
            <span>Категории APK</span>
            <button class="close-btn" onclick="toggleDrawer()">&times;</button>
        </div>
        <a href="#" class="drawer-item" onclick="filterCat('all'); toggleDrawer();">🔥 Все приложения</a>
"""

for cat in CATEGORIES:
    HTML_HEAD += f'        <a href="#" class="drawer-item" onclick="filterCat(\'{cat}\'); toggleDrawer();">{cat}</a>\n'

HTML_HEAD += """
    </div>
"""

def generate_index():
    cards = ""
    for app in ALL_APPS:
        cards += f"""
        <a href="{app['slug']}.html" class="app-card" data-name="{app['name'].lower()}" data-cat="{app['category']}">
            <div class="app-icon">{app['icon']}</div>
            <div class="app-body">
                <div class="app-title">{app['name']}</div>
                <div class="app-category">{app['category']} &bull; ★ {app['rating']}</div>
                <div class="app-desc">{app['desc']}</div>
            </div>
        </a>
        """

    html = HTML_HEAD.replace("{REFRAL_LINK}", REFRAL_LINK) + f"""
    <main class="container">
        <div class="promo-card">
            <div>
                <div class="promo-title">🔥 Партнерский бонус: Стабильный M3U Плейлист</div>
                <div class="promo-sub">1000+ каналов в высоком качестве, архив и быстрая работа. Заберите тест!</div>
            </div>
            <a href="{REFRAL_LINK}" target="_blank" class="promo-btn">Получить тест &rarr;</a>
        </div>

        <div style="margin-bottom: 1.5rem; font-size: 0.9rem; color: #64748b;" id="currentCatTitle">Автономный архив выкопанного софта (Всего: {len(ALL_APPS)})</div>

        <div class="grid" id="appsGrid">
            {cards}
        </div>
    </main>
    <footer class="footer">&copy; 2026 Git App WTF 🤨 — Бескомпромиссный парсер APK.</footer>
    <script>
        function toggleDrawer() { document.getElementById('catDrawer').classList.toggle('open'); }
        function filterCat(cat) {
            document.getElementById('currentCatTitle').innerText = cat === 'all' ? 'Все выкопанные приложения' : 'Категория: ' + cat;
            document.querySelectorAll('.app-card').forEach(card => {
                if (cat === 'all' || card.getAttribute('data-cat') === cat) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const val = e.target.value.toLowerCase();
            document.querySelectorAll('.app-card').forEach(card => {
                card.style.display = card.getAttribute('data-name').includes(val) ? 'flex' : 'none';
            });
        });
    </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_app_page(app):
    html = HTML_HEAD.replace("{REFRAL_LINK}", REFRAL_LINK) + f"""
    <main class="container" style="max-width: 800px;">
        <a href="index.html" style="color: #818cf8; font-weight: 600; font-size: 0.85rem; display: inline-block; margin-bottom: 1.5rem;">&larr; На главную</a>
        <div style="display: flex; gap: 1.5rem; align-items: center; margin-bottom: 2rem;">
            <div style="width: 5rem; height: 5rem; border-radius: 1.25rem; background: #020617; border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; font-size: 2.5rem;">{app['icon']}</div>
            <div>
                <h1 style="font-size: 1.85rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.3rem;">{app['name']}</h1>
                <div style="display: flex; gap: 0.75rem; font-size: 0.85rem; color: #94a3b8;">
                    <span style="color: #fbbf24; font-weight: 700;">★ {app['rating']}</span><span>•</span><span>Категория: {app['category']}</span>
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; margin-bottom: 2.5rem; flex-wrap: wrap;">
            <a href="{app['fallback_apk']}" target="_blank" style="background: linear-gradient(135deg, #f43f5e, #e11d48); color: #fff; padding: 0.85rem 1.75rem; border-radius: 0.85rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 15px rgba(244,63,94,0.35);">📥 Скачать APK (Прямой источник)</a>
            <a href="{REFRAL_LINK}" target="_blank" style="background: rgba(30,41,59,0.8); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); padding: 0.85rem 1.5rem; border-radius: 0.85rem; font-weight: 600;">🎁 Плейлист iSeeTV</a>
        </div>
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 1.25rem; padding: 1.75rem; margin-bottom: 2rem; line-height: 1.7;">
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.75rem;">Описание из источника</h2>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1.5rem;">{app['desc']}</p>
        </div>
    </main>
    <footer class="footer">&copy; 2026 Git App WTF 🤨 — Автономный архив.</footer>
    <script>function toggleDrawer() { document.getElementById('catDrawer').classList.toggle('open'); }</script>
</body>
</html>
"""
    with open(f"{app['slug']}.html", "w", encoding="utf-8") as f:
        f.write(html)

generate_index()
for app in ALL_APPS:
    generate_app_page(app)

print(f"Парсер отработал жестко. Выкопано и опубликовано приложений: {len(ALL_APPS)}")
