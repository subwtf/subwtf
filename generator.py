import json
import urllib.request

REFRAL_LINK = "https://iseetv.net/welcome/signup/cb26f9e15332cb38"

APPS_DATA = [
    {
        "slug": "televizo",
        "name": "Televizo",
        "badge": "TOP 🔥",
        "category": "IPTV Плееры",
        "rating": "4.9",
        "icon": "📺",
        "github_repo": "alexelec/Televizo",
        "fallback_apk": "https://github.com/alexelec/Televizo/releases",
        "desc": "Современный и мощный IPTV плеер для Android TV и смартфонов. Полная поддержка M3U и Xtream Codes API."
    },
    {
        "slug": "ott-navigator",
        "name": "OTT Navigator",
        "badge": "PRO ✨",
        "category": "Медиацентры",
        "rating": "4.8",
        "icon": "⚡",
        "github_repo": "",
        "fallback_apk": "https://ott-navigator.ru",
        "desc": "Продвинутый плеер с функцией архива передач, поддержкой нескольких плейлистов, картинкой-в-картинке и детальным EPG."
    },
    {
        "slug": "tvimate",
        "name": "TiviMate",
        "badge": "BEST 👑",
        "category": "Smart TV",
        "rating": "5.0",
        "icon": "🎬",
        "github_repo": "",
        "fallback_apk": "https://tvimate.com",
        "desc": "Премиальный интерфейс в стиле кабельного ТВ. Разработан специально для приставок и телевизоров с пультом ДУ."
    },
    {
        "slug": "iptv-smarters",
        "name": "IPTV Smarters Pro",
        "badge": "MULTI 📱",
        "category": "Android & Box",
        "rating": "4.7",
        "icon": "📲",
        "github_repo": "",
        "fallback_apk": "https://www.iptvsmarters.com",
        "desc": "Универсальный медиаплеер с поддержкой видео по запросу (VOD), сериалов и встроенного родительского контроля."
    },
    {
        "slug": "perfect-player",
        "name": "Perfect Player",
        "badge": "LITE 🚀",
        "category": "Android TV",
        "rating": "4.6",
        "icon": "📡",
        "github_repo": "",
        "fallback_apk": "http://www.niklabs.com",
        "desc": "Легковесный плеер для слабых ТВ-приставок. Минимальный расход ресурсов и мгновенный запуск M3U каналов."
    }
]

def fetch_github_release(repo):
    if not repo:
        return None
    try:
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        req = urllib.request.Request(url, headers={'User-Agent': 'TVStoreBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            for asset in data.get('assets', []):
                if asset['name'].endswith('.apk'):
                    return asset['browser_download_url']
            return data.get('html_url')
    except Exception as e:
        print(f"Ошибка GitHub API для {repo}: {e}")
    return None

HTML_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TV Store APK — Магазин приложений для Smart TV и Android Box</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #090d16;
            color: #f1f5f9;
            line-height: 1.5;
            min-height: 100vh;
        }
        a { color: inherit; text-decoration: none; }
        .header {
            position: sticky; top: 0; z-index: 50;
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 1rem 1.5rem;
            display: flex; align-items: center; justify-content: space-between; gap: 1rem;
        }
        .logo {
            display: flex; align-items: center; gap: 0.75rem;
            font-weight: 800; font-size: 1.25rem;
        }
        .logo-box {
            width: 2.4rem; height: 2.4rem; border-radius: 0.75rem;
            background: linear-gradient(135deg, #6366f1, #3b82f6);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.2rem; box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
        }
        .search-container { flex-grow: 1; max-width: 380px; position: relative; }
        .search-input {
            width: 100%; padding: 0.6rem 1rem 0.6rem 2.4rem;
            border-radius: 0.75rem; background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1); color: #fff;
            font-size: 0.875rem; outline: none;
        }
        .burger-btn { background: transparent; border: none; color: #fff; font-size: 1.5rem; cursor: pointer; display: block; }
        @media (min-width: 768px) { .burger-btn { display: none; } }
        .nav-links { display: none; gap: 1.5rem; font-weight: 600; font-size: 0.9rem; color: #94a3b8; }
        @media (min-width: 768px) { .nav-links { display: flex; align-items: center; } }
        .mobile-menu {
            display: none; position: fixed; top: 4.1rem; left: 0; right: 0;
            background: #0f172a; border-bottom: 1px solid rgba(255,255,255,0.1);
            padding: 1.25rem; z-index: 40; flex-direction: column; gap: 1rem;
        }
        .mobile-menu.active { display: flex; }
        .promo-card {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(30, 41, 59, 0.8));
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 1.25rem; padding: 1.75rem; margin: 1.5rem 0 2rem;
            display: flex; flex-direction: column; gap: 1.25rem; justify-content: space-between;
        }
        @media (min-width: 768px) { .promo-card { flex-direction: row; align-items: center; } }
        .promo-title { font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.4rem; }
        .promo-sub { font-size: 0.9rem; color: #94a3b8; }
        .promo-btn {
            background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff;
            padding: 0.85rem 1.75rem; border-radius: 0.75rem; font-weight: 700;
            white-space: nowrap; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35); text-align: center;
        }
        .container { max-width: 1100px; margin: 0 auto; padding: 1rem 1.25rem 4rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 1.25rem; }
        .app-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1.25rem; padding: 1.25rem;
            display: flex; gap: 1rem; transition: all 0.25s ease; position: relative;
        }
        .app-card:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(99, 102, 241, 0.4);
            transform: translateY(-4px);
        }
        .app-badge {
            position: absolute; top: 1rem; right: 1rem;
            font-size: 0.65rem; font-weight: 800; padding: 0.2rem 0.5rem;
            border-radius: 0.4rem; background: rgba(99, 102, 241, 0.2); color: #818cf8;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .app-icon {
            width: 3.75rem; height: 3.75rem; border-radius: 1rem;
            background: #020617; border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex; align-items: center; justify-content: center; font-size: 1.8rem; flex-shrink: 0;
        }
        .app-body { flex-grow: 1; min-width: 0; }
        .app-title { font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.2rem; }
        .app-category { font-size: 0.75rem; color: #64748b; font-weight: 600; margin-bottom: 0.5rem; }
        .app-desc { font-size: 0.825rem; color: #94a3b8; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .footer { border-top: 1px solid rgba(255, 255, 255, 0.08); padding: 2.5rem 1.25rem; text-align: center; color: #64748b; font-size: 0.85rem; }
    </style>
</head>
<body>
    <header class="header">
        <a href="index.html" class="logo">
            <div class="logo-box">📺</div>
            <div>TV Store<span style="color:#6366f1">.APK</span></div>
        </a>
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="Поиск приложений для TV...">
        </div>
        <nav class="nav-links">
            <a href="index.html">Главная</a>
            <a href="#catalog">Каталог</a>
            <a href="{REFRAL_LINK}" target="_blank" style="color: #818cf8;">🎁 Плейлист iSeeTV</a>
        </nav>
        <button class="burger-btn" onclick="toggleMenu()">☰</button>
    </header>
    <div class="mobile-menu" id="mobileMenu">
        <a href="index.html" style="color:#fff; font-weight:700;">Главная</a>
        <a href="#catalog" style="color:#94a3b8;">Каталог APK</a>
        <a href="{REFRAL_LINK}" target="_blank" style="color:#818cf8; font-weight:700;">🎁 Получить тест M3U</a>
    </div>
"""

def generate_index():
    cards = ""
    for app in APPS_DATA:
        cards += f"""
        <a href="{app['slug']}.html" class="app-card" data-name="{app['name'].lower()}">
            <span class="app-badge">{app['badge']}</span>
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
                <div class="promo-title">🔥 Стабильный M3U Плейлист для всех приложений TV Store</div>
                <div class="promo-sub">Более 1000+ каналов в UltraHD/4K качество, архив 7 дней и мгновенное переключение. Заберите бесплатный тест!</div>
            </div>
            <a href="{REFRAL_LINK}" target="_blank" class="promo-btn">Тестировать бесплатно &rarr;</a>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;" id="catalog">
            <h2 style="font-size: 1.35rem; font-weight: 800; color: #f8fafc;">Каталог приложений</h2>
            <span style="font-size: 0.85rem; color: #64748b;">Авто-обновление релизов</span>
        </div>
        <div class="grid" id="appsGrid">
            {cards}
        </div>
    </main>
    <footer class="footer">&copy; 2026 TV Store APK — Каталог дистрибутивов для Smart TV и Android устройств.</footer>
    <script>
        function toggleMenu() {{ document.getElementById('mobileMenu').classList.toggle('active'); }}
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
        <a href="index.html" style="color: #818cf8; font-weight: 600; font-size: 0.85rem; display: inline-block; margin-bottom: 1.5rem;">&larr; Назад в каталог TV Store</a>
        <div style="display: flex; gap: 1.5rem; align-items: center; margin-bottom: 2rem;">
            <div style="width: 5rem; height: 5rem; border-radius: 1.25rem; background: #020617; border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; font-size: 2.5rem;">{app['icon']}</div>
            <div>
                <h1 style="font-size: 1.85rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.3rem;">{app['name']}</h1>
                <div style="display: flex; gap: 0.75rem; font-size: 0.85rem; color: #94a3b8;">
                    <span style="color: #fbbf24; font-weight: 700;">★ {app['rating']}</span><span>•</span><span>{app['category']}</span>
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; margin-bottom: 2.5rem; flex-wrap: wrap;">
            <a href="{download_url}" target="_blank" style="background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; padding: 0.85rem 1.75rem; border-radius: 0.85rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 15px rgba(99,102,241,0.35);">📥 Скачать APK (Прямая ссылка)</a>
            <a href="{REFRAL_LINK}" target="_blank" style="background: rgba(30,41,59,0.8); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); padding: 0.85rem 1.5rem; border-radius: 0.85rem; font-weight: 600;">🎁 Плейлист iSeeTV для {app['name']}</a>
        </div>
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 1.25rem; padding: 1.75rem; margin-bottom: 2rem; line-height: 1.7;">
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.75rem;">Описание приложения</h2>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1.5rem;">{app['desc']}</p>
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.75rem;">Как подключить M3U плейлист в {app['name']}</h2>
            <ol style="color: #cbd5e1; font-size: 0.9rem; padding-left: 1.2rem; display: flex; flex-direction: column; gap: 0.5rem;">
                <li>Получите персональную M3U-ссылку или параметры подключения в <a href="{REFRAL_LINK}" target="_blank" style="color: #818cf8; font-weight: 700;">сервисе iSeeTV</a>.</li>
                <li>Запустите {app['name']} на телевизоре или ТВ-приставке.</li>
                <li>Перейдите в меню <b>Настройки &rarr; Плейлисты &rarr; Добавить</b>.</li>
                <li>Вставьте вашу ссылку и сохраните изменения.</li>
            </ol>
        </div>
        <div class="promo-card">
            <div>
                <div class="promo-title">Нужен проверенный список каналов?</div>
                <div class="promo-desc">Подключите iSeeTV — более 1000+ каналов без буферизации, с архивом и идеальным качеством.</div>
            </div>
            <a href="{REFRAL_LINK}" target="_blank" class="promo-btn">Подключить &rarr;</a>
        </div>
    </main>
    <footer class="footer">&copy; 2026 TV Store APK — Официальные сборки и инструкции.</footer>
    <script>function toggleMenu() {{ document.getElementById('mobileMenu').classList.toggle('active'); }}</script>
</body>
</html>
"""
    with open(f"{app['slug']}.html", "w", encoding="utf-8") as f:
        f.write(html)

generate_index()
for app in APPS_DATA:
    generate_app_page(app)

print("Генерация TV Store завершена успешно!")
