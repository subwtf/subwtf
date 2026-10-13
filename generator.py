import json
import urllib.request
import urllib.parse
import re
import random
import os
from datetime import datetime

REFRAL_LINK = "https://iseetv.net/welcome/signup/cb26f9e15332cb38"

CATEGORIES = [
    "IPTV Плееры", "Медиацентры", "Smart TV", "Кино и Сериалы", 
    "Видеоплееры", "Аудио и Радио", "Утилиты TV", "Файловые менеджеры",
    "Браузеры", "Лаунчеры", "Оптимизация", "Безопасность", 
    "Тесты скорости", "Управление ДУ", "Инструменты", "Системные",
    "Игровые эмуляторы", "Другое"
]

APPS_DATA = [
    {
        "slug": "televizo",
        "name": "Televizo",
        "category": "IPTV Плееры",
        "rating": "4.9",
        "icon": "📺",
        "file_size": "18.4 MB",
        "date": "12.10.2026",
        "fallback_apk": "https://televizo.net/apk/televizo.apk",
        "desc": "Современный и мощный IPTV плеер для Android TV и смартфонов. Полная поддержка плейлистов M3U и электронного гида передач (EPG)."
    },
    {
        "slug": "smarttube",
        "name": "SmartTube",
        "category": "Smart TV",
        "rating": "5.0",
        "icon": "🔴",
        "file_size": "24.1 MB",
        "date": "13.10.2026",
        "fallback_apk": "https://github.com/yuliskov/SmartTube/releases/download/latest/SmartTube_stable.apk",
        "desc": "Альтернативный клиент YouTube для Android TV приставок и телевизоров. Автоматический пропуск спонсорских вставок и отсутствие рекламы."
    },
    {
        "slug": "ott-navigator",
        "name": "OTT Navigator",
        "category": "Медиацентры",
        "rating": "4.8",
        "icon": "⚡",
        "file_size": "31.0 MB",
        "date": "10.10.2026",
        "fallback_apk": "https://ott-navigator.com",
        "desc": "Продвинутый просмотрщик IPTV с поддержкой архивов, удобной сеткой каналов и гибкой настройкой интерфейса под пульт ДУ."
    }
]

def ruthless_scraper():
    queries = ["android apk player", "smart tv launcher apk", "iptv client release apk", "tools utility android apk"]
    scraped = []
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    for q in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=10"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'})
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read().decode())
                for item in data.get('items', []):
                    name = item.get('name')
                    html_url = item.get('html_url')
                    desc = item.get('description') or "Автоматически извлеченный APK-пакет из открытого репозитория GitHub."
                    
                    slug = re.sub(r'[^a-zA-Z0-9]', '-', name).lower().strip('-')
                    if not slug or len(slug) < 2 or any(a['slug'] == slug for a in APPS_DATA + scraped):
                        continue
                    
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
                        "rating": str(round(random.uniform(4.5, 5.0), 1)),
                        "icon": random.choice(["📦", "⚡", "🔥", "🚀", "🛠️"]),
                        "file_size": f"{random.randint(8, 45)}.{random.randint(1,9)} MB",
                        "date": current_date,
                        "fallback_apk": f"{html_url}/releases",
                        "desc": desc[:140] + "..."
                    })
        except Exception:
            continue
    return scraped

ALL_APPS = APPS_DATA + ruthless_scraper()

LIGHT_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_title}</title>
    <meta name="description" content="{meta_desc}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #1e293b; line-height: 1.5; min-height: 100vh; }
        a { color: inherit; text-decoration: none; }
        
        /* Шапкка в светлом стиле */
        .header { position: sticky; top: 0; z-index: 50; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid #e2e8f0; padding: 0.85rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
        .logo { display: flex; align-items: center; gap: 0.6rem; font-weight: 800; font-size: 1.15rem; color: #0f172a; }
        .logo-box { width: 2.2rem; height: 2.2rem; border-radius: 0.6rem; background: linear-gradient(135deg, #3b82f6, #6366f1); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #fff; }
        
        .search-container { flex-grow: 1; max-width: 320px; }
        .search-input { width: 100%; padding: 0.5rem 0.85rem; border-radius: 0.6rem; background: #f1f5f9; border: 1px solid #cbd5e1; color: #0f172a; font-size: 0.85rem; outline: none; }
        .search-input:focus { border-color: #3b82f6; background: #fff; }
        
        .burger-btn { background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; padding: 0.45rem 0.65rem; border-radius: 0.5rem; cursor: pointer; font-size: 1.1rem; }

        /* Выпадающий бургер категорий */
        .drawer { position: fixed; top: 0; right: -300px; width: 300px; height: 100vh; background: #ffffff; border-left: 1px solid #e2e8f0; z-index: 100; transition: right 0.3s ease; padding: 1.5rem; overflow-y: auto; box-shadow: -5px 0 25px rgba(0,0,0,0.05); }
        .drawer.open { right: 0; }
        .drawer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; font-weight: 800; font-size: 1.05rem; color: #0f172a; }
        .close-btn { background: none; border: none; color: #64748b; font-size: 1.4rem; cursor: pointer; }
        .drawer-item { display: block; padding: 0.5rem 0.75rem; border-radius: 0.4rem; color: #475569; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.2rem; transition: all 0.15s; }
        .drawer-item:hover { background: #eff6ff; color: #2563eb; }

        .container { max-width: 1000px; margin: 0 auto; padding: 1rem 1rem 3rem; }
        
        /* Сетка: ровно 2 карточки в ряд на мобильных и ПК */
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.85rem; }
        
        /* Карточки приложений в стиле Trashbox / APKPure */
        .app-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 0.85rem; display: flex; flex-direction: column; justify-content: space-between; gap: 0.6rem; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .app-card:hover { border-color: #3b82f6; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59,130,246,0.08); }
        
        .card-top { display: flex; gap: 0.6rem; align-items: flex-start; }
        .app-icon { width: 3rem; height: 3rem; border-radius: 0.6rem; background: #f1f5f9; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0; }
        .app-info { min-width: 0; flex-grow: 1; }
        .app-title { font-size: 0.9rem; font-weight: 700; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 0.1rem; }
        .app-category { font-size: 0.7rem; color: #64748b; font-weight: 600; }
        
        .app-desc { font-size: 0.75rem; color: #475569; line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        
        .card-meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.65rem; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 0.5rem; margin-top: auto; }
        
        .footer { border-top: 1px solid #e2e8f0; padding: 2rem 1rem; text-align: center; color: #64748b; font-size: 0.8rem; background: #fff; margin-top: 2rem; }
    </style>
</head>
<body>
    <header class="header">
        <a href="index.html" class="logo">
            <div class="logo-box">🤨</div>
            <div>Git App <span style="color:#2563eb">WTF</span></div>
        </a>
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="Поиск APK...">
        </div>
        <button class="burger-btn" onclick="toggleDrawer()">☰</button>
    </header>

    <div class="drawer" id="catDrawer">
        <div class="drawer-header">
            <span>Категории софта</span>
            <button class="close-btn" onclick="toggleDrawer()">&times;</button>
        </div>
        <a href="#" class="drawer-item" onclick="filterCat('all'); toggleDrawer();">🔥 Все приложения</a>
"""

for cat in CATEGORIES:
    LIGHT_HEAD += f'        <a href="#" class="drawer-item" onclick="filterCat(\'{cat}\'); toggleDrawer();">{cat}</a>\n'

LIGHT_HEAD += """
    </div>
"""

def generate_index():
    cards = ""
    for app in ALL_APPS:
        cards += f"""
        <a href="{app['slug']}.html" class="app-card" data-name="{app['name'].lower()}" data-cat="{app['category']}">
            <div class="card-top">
                <div class="app-icon">{app['icon']}</div>
                <div class="app-info">
                    <div class="app-title">{app['name']}</div>
                    <div class="app-category">{app['category']} &bull; ★ {app['rating']}</div>
                </div>
            </div>
            <div class="app-desc">{app['desc']}</div>
            <div class="card-meta">
                <span>💾 {app['file_size']}</span>
                <span>📅 {app['date']}</span>
            </div>
        </a>
        """

    head_html = LIGHT_HEAD.format(
        meta_title="Git App WTF 🤨 — Скачать APK для Android и Smart TV бесплатно",
        meta_desc="Каталог полезных Android и Smart TV приложений. Свежие APK файлы с размерами и описанием."
    )
    
    html = head_html + f"""
    <main class="container">
        <div style="background: linear-gradient(135deg, #eff6ff, #f1f5f9); border: 1px solid #bfdbfe; border-radius: 0.85rem; padding: 1.15rem; margin-bottom: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem;">
            <div>
                <div style="font-size: 0.95rem; font-weight: 800; color: #1e3a8a; margin-bottom: 0.2rem;">🔥 Партнерский бонус: IPTV Плейлист</div>
                <div style="font-size: 0.75rem; color: #475569;">1000+ каналов в HD/4K качестве для любых плееров. Попробуйте тест бесплатно!</div>
            </div>
            <a href="{REFRAL_LINK}" target="_blank" style="background: #2563eb; color: #fff; padding: 0.55rem 1rem; border-radius: 0.5rem; font-weight: 700; font-size: 0.75rem; text-align: center; box-shadow: 0 2px 8px rgba(37,99,235,0.2);">Получить плейлист &rarr;</a>
        </div>

        <div style="margin-bottom: 1rem; font-size: 0.8rem; color: #64748b;" id="currentCatTitle">Все приложения в каталоге ({len(ALL_APPS)})</div>

        <div class="grid" id="appsGrid">
            {cards}
        </div>
    </main>
    <footer class="footer">&copy; 2026 Git App WTF 🤨 — Каталог APK дистрибутивов.</footer>
    <script>
        function toggleDrawer() { document.getElementById('catDrawer').classList.toggle('open'); }
        function filterCat(cat) {
            document.getElementById('currentCatTitle').innerText = cat === 'all' ? 'Все приложения в каталоге' : 'Категория: ' + cat;
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
    head_html = LIGHT_HEAD.format(
        meta_title=f"Скачать {app['name']} APK бесплатно — Git App WTF",
        meta_desc=f"Скачать последнюю версию {app['name']} ({app['file_size']}) для Android и Smart TV. {app['desc'][:80]}"
    )
    
    html = head_html + f"""
    <main class="container" style="max-width: 750px;">
        <a href="index.html" style="color: #2563eb; font-weight: 600; font-size: 0.8rem; display: inline-block; margin-bottom: 1rem;">&larr; На главную в каталог</a>
        
        <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 1.25rem; margin-bottom: 1rem; display: flex; gap: 1rem; align-items: center;">
            <div style="width: 4rem; height: 4rem; border-radius: 0.75rem; background: #f1f5f9; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: center; font-size: 2rem; flex-shrink: 0;">{app['icon']}</div>
            <div>
                <h1 style="font-size: 1.35rem; font-weight: 800; color: #0f172a; margin-bottom: 0.2rem;">{app['name']}</h1>
                <div style="display: flex; gap: 0.5rem; font-size: 0.75rem; color: #64748b; flex-wrap: wrap;">
                    <span style="color: #d97706; font-weight: 700;">★ {app['rating']}</span>
                    <span>&bull;</span>
                    <span>{app['category']}</span>
                    <span>&bull;</span>
                    <span>Размер: <b>{app['file_size']}</b></span>
                    <span>&bull;</span>
                    <span>Обновлено: {app['date']}</span>
                </div>
            </div>
        </div>

        <!-- Кнопка прямой загрузки на странице приложения -->
        <div style="margin-bottom: 1.5rem;">
            <a href="{app['fallback_apk']}" style="background: #2563eb; color: #fff; padding: 0.85rem 1.5rem; border-radius: 0.75rem; font-weight: 700; font-size: 0.9rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; box-shadow: 0 4px 12px rgba(37,99,235,0.25);">📥 Скачать APK файл ({app['file_size']})</a>
            <div style="text-align: center; font-size: 0.7rem; color: #94a3b8; margin-top: 0.4rem;">Прямая безопасная ссылка на мгновенную загрузку</div>
        </div>

        <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 1.25rem; margin-bottom: 1.25rem; line-height: 1.6;">
            <h2 style="font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Описание и возможности {app['name']}</h2>
            <p style="color: #334155; font-size: 0.85rem; margin-bottom: 1rem;">{app['desc']}</p>
            
            <h3 style="font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-bottom: 0.4rem;">Как установить APK на Android / Smart TV</h3>
            <ol style="color: #475569; font-size: 0.8rem; padding-left: 1.1rem; display: flex; flex-direction: column; gap: 0.3rem;">
                <li>Нажмите кнопку выше для скачивания APK файла на устройство.</li>
                <li>Разрешите установку из неизвестных источников в настройках безопасности.</li>
                <li>Запустите загруженный файл для инсталляции приложения.</li>
            </ol>
        </div>

        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.85rem; padding: 1.15rem; display: flex; flex-direction: column; gap: 0.6rem;">
            <div style="font-size: 0.9rem; font-weight: 800; color: #1e3a8a;">Рекомендуем для просмотра ТВ</div>
            <div style="font-size: 0.75rem; color: #475569;">Подключите стабильный сервис iSeeTV и получите доступ к сотням каналов в отличном качестве.</div>
            <a href="{REFRAL_LINK}" target="_blank" style="background: #2563eb; color: #fff; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 700; font-size: 0.75rem; text-align: center; display: inline-block; width: fit-content;">Подключить iSeeTV &rarr;</a>
        </div>
    </main>
    <footer class="footer">&copy; 2026 Git App WTF 🤨 — Официальные дистрибутивы.</footer>
    <script>function toggleDrawer() { document.getElementById('catDrawer').classList.toggle('open'); }</script>
</body>
</html>
"""
    with open(f"{app['slug']}.html", "w", encoding="utf-8") as f:
        f.write(html)

generate_index()
for app in ALL_APPS:
    generate_app_page(app)

print(f"Светлый интерфейс в стиле APKPure/Trashbox развернут. Обработано приложений: {len(ALL_APPS)}")
