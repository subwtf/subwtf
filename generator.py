import json
import urllib.request
import os

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
        "github_repo": "alexelec/Televizo",
        "fallback_apk": "https://televizo.net/apk/televizo.apk",
        "desc": "Современный и мощный IPTV плеер для Android TV и смартфонов. Поддержка M3U и Xtream Codes."
    },
    {
        "slug": "smarttube",
        "name": "SmartTube",
        "category": "Smart TV",
        "rating": "5.0",
        "icon": "🔴",
        "github_repo": "yuliskov/SmartTube",
        "fallback_apk": "https://github.com/yuliskov/SmartTube/releases",
        "desc": "Продвинутый клиент YouTube для Android TV и приставок с автопропуском интеграций и без рекламы."
    },
    {
        "slug": "ott-navigator",
        "name": "OTT Navigator",
        "category": "Медиацентры",
        "rating": "4.8",
        "icon": "⚡",
        "github_repo": "",
        "fallback_apk": "https://ott-navigator.com",
        "desc": "Мощный плеер с функцией архива передач, поддержкой нескольких плейлистов и детальным EPG гидом."
    },
    {
        "slug": "tvimate",
        "name": "TiviMate",
        "category": "IPTV Плееры",
        "rating": "4.9",
        "icon": "🎬",
        "github_repo": "",
        "fallback_apk": "https://tvimate.com",
        "desc": "Премиальный интерфейс в стиле кабельного ТВ. Идеален для ТВ-приставок и пультов ДУ."
    },
    {
        "slug": "kodi",
        "name": "Kodi Media Center",
        "category": "Медиацентры",
        "rating": "4.7",
        "icon": "📦",
        "github_repo": "xbmc/xbmc",
        "fallback_apk": "https://kodi.tv/download/android",
        "desc": "Бесплатный кроссплатформенный медиацентр с открытым исходным кодом для воспроизведения видео и ТВ."
    },
    {
        "slug": "vlc-android",
        "name": "VLC for Android",
        "category": "Видеоплееры",
        "rating": "4.8",
        "icon": "🧡",
        "github_repo": "videolan/vlc-android",
        "fallback_apk": "https://www.videolan.org/vlc/download-android.html",
        "desc": "Универсальный медиаплеер, воспроизводящий большинство локальных видео и аудио файлов, а также сетевые потоки."
    }
]

def fetch_github_release(repo):
    if not repo:
        return None
    try:
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        req = urllib.request.Request(url, headers={'User-Agent': 'TVStoreBot/2.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            for asset in data.get('assets', []):
                if asset['name'].endswith('.apk'):
                    return asset['browser_download_url']
            return data.get('html_url')
    except Exception:
        pass
    return None

HTML_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TV Store APK — Каталог приложений для Smart TV</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #090d16; color: #f1f5f9; line-height: 1.5; min-height: 100vh; }
        a { color: inherit; text-decoration: none; }
        .header { position: sticky; top: 0; z-index: 50; background: rgba(9, 13, 22, 0.85); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.08); padding: 1rem 1.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
        .logo { display: flex; align-items: center; gap: 0.75rem; font-weight: 800; font-size: 1.25rem; }
        .logo-box { width: 2.4rem; height: 2.4rem; border-radius: 0.75rem; background: linear-gradient(135deg, #6366f1, #3b82f6); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
        .search-container { flex-grow: 1; max-width: 380px; }
        .search-input { width: 100%; padding: 0.6rem 1rem; border-radius: 0.75rem; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); color: #fff; font-size: 0.875rem; outline: none; }
        .cat-scroll { display: flex; gap: 0.5rem; overflow-x: auto; padding: 1rem 0; margin-bottom: 1.5rem; scrollbar-width: none; }
        .cat-chip { padding: 0.4rem 0.85rem; border-radius: 2rem; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.8rem; font-weight: 600; white-space: nowrap; color: #94a3b8; cursor: pointer; }
        .cat-chip:hover, .cat-chip.active { background: #6366f1; color: #fff; border-color: #6366f1; }
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
            <div class="logo-box">📱</div>
            <div>TV Store<span style="color:#6366f1">.APK</span></div>
        </a>
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="Поиск приложений...">
        </div>
    </header>
"""

def generate_index():
    chips_html = '<div class="cat-chip active" onclick="filterCat(\'all\')">Все (18)</div>'
    for cat in CATEGORIES:
        chips_html += f'<div class="cat-chip" onclick="filterCat(\'{cat}\')">{cat}</div>'

    cards = ""
    for app in APPS_DATA:
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
                <div class="promo-title">🔥 Стабильный M3U Плейлист для всех ТВ-плееров</div>
                <div class="promo-sub">1000+ каналов в 4K/FullHD качества, архив передач и мгновенное переключение. Заберите бесплатный тест!</div>
            </div>
            <a href="{REFRAL_LINK}" target="_blank" class="promo-btn">Подключить тест &rarr;</a>
        </div>

        <div class="cat-scroll">
            {chips_html}
        </div>

        <div class="grid" id="appsGrid">
            {cards}
        </div>
    </main>
    <footer class="footer">&copy; 2026 TV Store APK — Каталог APK приложений.</footer>
    <script>
        function filterCat(cat) {{
            document.querySelectorAll('.cat-chip').forEach(el => el.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.app-card').forEach(card => {{
                if (cat === 'all' || card.getAttribute('data-cat') === cat) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const val = e.target.value.toLowerCase();
            document.querySelectorAll('.app-card').forEach(card => {{
                card.style.display = card.getAttribute('data-name').includes(val) ? 'flex' : 'none';
            }});
        }});
    </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_app_page(app):
    download_url = fetch_github_release(app['github_repo']) or app['fallback_apk']
    html = HTML_HEAD.replace("{REFRAL_LINK}", REFRAL_LINK) + f"""
    <main class="container" style="max-width: 800px;">
        <a href="index.html" style="color: #818cf8; font-weight: 600; font-size: 0.85rem; display: inline-block; margin-bottom: 1.5rem;">&larr; Назад в каталог</a>
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
            <a href="{download_url}" target="_blank" style="background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; padding: 0.85rem 1.75rem; border-radius: 0.85rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 15px rgba(99,102,241,0.35);">📥 Скачать APK (Официальный)</a>
            <a href="{REFRAL_LINK}" target="_blank" style="background: rgba(30,41,59,0.8); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); padding: 0.85rem 1.5rem; border-radius: 0.85rem; font-weight: 600;">🎁 Плейлист iSeeTV</a>
        </div>
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 1.25rem; padding: 1.75rem; margin-bottom: 2rem; line-height: 1.7;">
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.75rem;">Описание и возможности</h2>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1.5rem;">{app['desc']}</p>
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.75rem;">Инструкция по установке и настройке</h2>
            <ol style="color: #cbd5e1; font-size: 0.9rem; padding-left: 1.2rem; display: flex; flex-direction: column; gap: 0.5rem;">
                <li>Скачайте и установите APK-файл приложения {app['name']} на ваше Android TV или устройство.</li>
                <li>Получите персональную M3U-ссылку или учетные данные в <a href="{REFRAL_LINK}" target="_blank" style="color: #818cf8; font-weight: 700;">сервисе iSeeTV</a>.</li>
                <li>Запустите {app['name']}, откройте Настройки &rarr; Плейлисты и добавьте вашу ссылку.</li>
            </ol>
        </div>
        <div class="promo-card">
            <div>
                <div class="promo-title">Нужен проверенный список каналов?</div>
                <div class="promo-desc">Подключите iSeeTV — более 1000+ каналов без буферизации, с архивом и отличным качеством.</div>
            </div>
            <a href="{REFRAL_LINK}" target="_blank" class="promo-btn">Подключить &rarr;</a>
        </div>
    </main>
    <footer class="footer">&copy; 2026 TV Store APK — Каталог приложений.</footer>
</body>
</html>
"""
    with open(f"{app['slug']}.html", "w", encoding="utf-8") as f:
        f.write(html)

generate_index()
for app in APPS_DATA:
    generate_app_page(app)

print("Каталог TV Store успешно собран!")
