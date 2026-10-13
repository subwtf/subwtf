import json, urllib.request, urllib.parse, re, random, os
from datetime import datetime

REFRAL_LINK = "https://iseetv.net/welcome/signup/cb26f9e15332cb38"
CATEGORIES = ["IPTV Плееры", "Медиацентры", "Smart TV", "Кино и Сериалы", "Видеоплееры", "Аудио и Радио", "Утилиты TV", "Файловые менеджеры", "Браузеры", "Лаунчеры", "Оптимизация", "Безопасность", "Тесты скорости", "Управление ДУ", "Инструменты", "Системные", "Игровые эмуляторы", "Другое"]

APPS_DATA = [
    {"slug": "televizo", "name": "Televizo", "category": "IPTV Плееры", "rating": "4.9", "icon": "📺", "file_size": "18.4 MB", "date": "12.10.2026", "fallback_apk": "https://televizo.net/apk/televizo.apk", "desc": "Современный и мощный IPTV плеер для Android TV и смартфонов. Поддержка M3U и EPG."},
    {"slug": "smarttube", "name": "SmartTube", "category": "Smart TV", "rating": "5.0", "icon": "🔴", "file_size": "24.1 MB", "date": "13.10.2026", "fallback_apk": "https://github.com/yuliskov/SmartTube/releases", "desc": "YouTube клиент без рекламы и с автопропуском спонсоров для Smart TV."},
    {"slug": "ott-navigator", "name": "OTT Navigator", "category": "Медиацентры", "rating": "4.8", "icon": "⚡", "file_size": "31.0 MB", "date": "10.10.2026", "fallback_apk": "https://ott-navigator.com", "desc": "Продвинутый просмотрщик IPTV с поддержкой архивов и гибкой настройкой интерфейса."}
]

def ruthless_scraper():
    queries = ["android apk player", "smart tv launcher apk", "iptv client release apk"]
    scraped = []
    current_date = datetime.now().strftime("%d.%m.%Y")
    for q in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=10"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=6) as response:
                data = json.loads(response.read().decode())
                for item in data.get("items", []):
                    name = item.get("name")
                    html_url = item.get("html_url")
                    desc = item.get("description") or "Автоматически извлеченный APK-пакет из GitHub."
                    slug = re.sub(r"[^a-zA-Z0-9]", "-", name).lower().strip("-")
                    if not slug or len(slug) < 2 or any(a["slug"] == slug for a in APPS_DATA + scraped): continue
                    scraped.append({
                        "slug": slug, "name": name, "category": "Smart TV", "rating": str(round(random.uniform(4.5, 5.0), 1)),
                        "icon": random.choice(["📦", "⚡", "🔥", "🚀"]), "file_size": f"{random.randint(8, 45)}.{random.randint(1,9)} MB",
                        "date": current_date, "fallback_apk": f"{html_url}/releases", "desc": desc[:140] + "..."
                    })
        except: continue
    return scraped

ALL_APPS = APPS_DATA + ruthless_scraper()

LIGHT_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_title}</title>
    <meta name="description" content="{meta_desc}">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #1e293b; line-height: 1.5; min-height: 100vh; }
        a { color: inherit; text-decoration: none; }
        .header { position: sticky; top: 0; z-index: 50; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border-bottom: 1px solid #e2e8f0; padding: 0.85rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
        .logo { display: flex; align-items: center; gap: 0.6rem; font-weight: 800; font-size: 1.15rem; color: #0f172a; }
        .logo-box { width: 2.2rem; height: 2.2rem; border-radius: 0.6rem; background: linear-gradient(135deg, #3b82f6, #6366f1); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #fff; }
        .search-container { flex-grow: 1; max-width: 320px; }
        .search-input { width: 100%; padding: 0.5rem 0.85rem; border-radius: 0.6rem; background: #f1f5f9; border: 1px solid #cbd5e1; color: #0f172a; font-size: 0.85rem; outline: none; }
        .container { max-width: 1000px; margin: 0 auto; padding: 1rem 1rem 3rem; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.85rem; }
        .app-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 0.85rem; display: flex; flex-direction: column; justify-content: space-between; gap: 0.6rem; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .app-card:hover { border-color: #3b82f6; transform: translateY(-2px); }
        .card-top { display: flex; gap: 0.6rem; align-items: flex-start; }
        .app-icon { width: 3rem; height: 3rem; border-radius: 0.6rem; background: #f1f5f9; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0; }
        .app-title { font-size: 0.9rem; font-weight: 700; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .app-category { font-size: 0.7rem; color: #64748b; font-weight: 600; }
        .app-desc { font-size: 0.75rem; color: #475569; line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .card-meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.65rem; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 0.5rem; margin-top: auto; }
        .footer { border-top: 1px solid #e2e8f0; padding: 2rem 1rem; text-align: center; color: #64748b; font-size: 0.8rem; background: #fff; margin-top: 2rem; }
    </style>
</head>
<body>
    <header class="header">
        <a href="index.html" class="logo"><div class="logo-box">🤨</div><div>Git App <span style="color:#2563eb">WTF</span></div></a>
        <div class="search-container"><input type="text" id="searchInput" class="search-input" placeholder="Поиск APK..."></div>
    </header>
"""

def generate_index():
    cards = ""
    for app in ALL_APPS:
        cards += f"""
        <a href="{app[slug]}.html" class="app-card">
            <div class="card-top">
                <div class="app-icon">{app[icon]}</div>
                <div><div class="app-title">{app[name]}</div><div class="app-category">{app[category]} &bull; ★ {app[rating]}</div></div>
            </div>
            <div class="app-desc">{app[desc]}</div>
            <div class="card-meta"><span>💾 {app[file_size]}</span><span>📅 {app[date]}</span></div>
        </a>
        """
    head = LIGHT_HEAD.format(meta_title="Git App WTF 🤨 — Скачать APK для Android и Smart TV", meta_desc="Каталог полезных Android и Smart TV приложений.")
    html = head + f"""
    <main class="container">
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.85rem; padding: 1.15rem; margin-bottom: 1.25rem;">
            <div style="font-size: 0.95rem; font-weight: 800; color: #1e3a8a;">🔥 Партнерский бонус: IPTV Плейлист</div>
            <div style="font-size: 0.75rem; color: #475569; margin-bottom: 0.5rem;">1000+ каналов в HD/4K качестве.</div>
            <a href="{REFRAL_LINK}" target="_blank" style="background: #2563eb; color: #fff; padding: 0.55rem 1rem; border-radius: 0.5rem; font-weight: 700; font-size: 0.75rem; display: inline-block;">Получить плейлист &rarr;</a>
        </div>
        <div class="grid">{cards}</div>
    </main>
    <footer class="footer">&copy; 2026 Git App WTF 🤨 — Каталог APK дистрибутивов.</footer>
</body>
</html>"""
    open("index.html", "w", encoding="utf-8").write(html)

def generate_app_pages():
    for app in ALL_APPS:
        head = LIGHT_HEAD.format(meta_title=f"Скачать {app[name]} APK бесплатно — Git App WTF", meta_desc=f"Скачать последнюю версию {app[name]} ({app[file_size]}).")
        html = head + f"""
        <main class="container" style="max-width: 750px;">
            <a href="index.html" style="color: #2563eb; font-weight: 600; font-size: 0.8rem; display: inline-block; margin-bottom: 1rem;">&larr; На главную</a>
            <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 1.25rem; margin-bottom: 1rem; display: flex; gap: 1rem; align-items: center;">
                <div style="width: 4rem; height: 4rem; border-radius: 0.75rem; background: #f1f5f9; display: flex; align-items: center; justify-content: center; font-size: 2rem;">{app[icon]}</div>
                <div>
                    <h1 style="font-size: 1.35rem; font-weight: 800; color: #0f172a;">{app[name]}</h1>
                    <div style="font-size: 0.75rem; color: #64748b;">★ {app[rating]} &bull; {app[category]} &bull; 💾 {app[file_size]} &bull; 📅 {app[date]}</div>
                </div>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <a href="{app[fallback_apk]}" style="background: #2563eb; color: #fff; padding: 0.85rem 1.5rem; border-radius: 0.75rem; font-weight: 700; font-size: 0.9rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">📥 Скачать APK файл ({app[file_size]})</a>
            </div>
            <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 1.25rem; line-height: 1.6;">
                <h2 style="font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Описание</h2>
                <p style="color: #334155; font-size: 0.85rem;">{app[desc]}</p>
            </div>
        </main>
        <footer class="footer">&copy; 2026 Git App WTF 🤨.</footer>
    </body>
    </html>"""
        open(f"{app[slug]}.html", "w", encoding="utf-8").write(html)

generate_index()
generate_app_pages()
print("Светлый сайт пересобран!")
