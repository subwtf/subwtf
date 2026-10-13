import json, os

DB_FILE = "database.json"

def get_smart_icon(app):
    icon_url = app.get("icon_url", "")
    if icon_url and "githubassets.com" not in icon_url and "avatars.githubusercontent.com" not in icon_url:
        return icon_url
    name = app.get("name", "APK")
    colors = ["10b981", "3b82f6", "6366f1", "8b5cf6", "ec4899", "f59e0b", "14b8a6"]
    bg_color = colors[len(name) % len(colors)]
    return f"https://ui-avatars.com/api/?name={urllib_quote(name)}&background={bg_color}&color=fff&size=128&bold=true&font-size=0.55&rounded=true"

import urllib.parse
def urllib_quote(s):
    return urllib.parse.quote(s)

def generate():
    if not os.path.exists(DB_FILE):
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    apps = db.get("apps", [])
    categories = sorted(list(set(app.get("category", "Утилиты") for app in apps)))

    index_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APKPure Style — Каталог приложений APK</title>
    <style>
        :root {{
            --bg: #f5f6f7;
            --card-bg: #ffffff;
            --text: #222222;
            --text-light: #777777;
            --accent: #00ce84;
            --accent-hover: #00b372;
            --border: #e6e6e6;
        }}
        body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; }}
        
        /* Шапка в стиле APKPure */
        header {{ background: #ffffff; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
        .header-left {{ display: flex; align-items: center; gap: 15px; }}
        .burger {{ background: none; border: none; font-size: 1.4rem; cursor: pointer; color: var(--text); }}
        .logo {{ font-size: 1.25rem; font-weight: 800; color: var(--text); text-decoration: none; display: flex; align-items: center; }}
        .logo span {{ color: var(--accent); margin-left: 2px; }}
        
        /* Поиск */
        .search-container {{ flex: 1; max-width: 500px; margin: 0 20px; position: relative; }}
        .search-input {{ width: 100%; padding: 10px 15px 10px 40px; border: 1px solid var(--border); border-radius: 24px; background: #f8f9fa; font-size: 0.95rem; outline: none; transition: 0.2s; box-sizing: border-box; }}
        .search-input:focus {{ border-color: var(--accent); background: #fff; box-shadow: 0 0 0 3px rgba(0,206,132,0.1); }}
        .search-icon {{ position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-light); font-size: 0.95rem; }}

        /* Бургер меню */
        .sidebar {{ position: fixed; top: 0; left: -300px; width: 280px; height: 100%; background: #ffffff; box-shadow: 5px 0 20px rgba(0,0,0,0.1); z-index: 1000; transition: 0.3s ease; padding: 20px; box-sizing: border-box; overflow-y: auto; }}
        .sidebar.open {{ left: 0; }}
        .sidebar-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; font-size: 1.1rem; font-weight: bold; border-bottom: 1px solid var(--border); padding-bottom: 10px; }}
        .close-btn {{ background: none; border: none; font-size: 1.3rem; cursor: pointer; color: var(--text-light); }}
        .cat-item {{ display: flex; align-items: center; gap: 10px; padding: 12px 15px; color: var(--text); text-decoration: none; border-radius: 10px; margin-bottom: 6px; font-weight: 500; transition: 0.2s; }}
        .cat-item:hover {{ background: #f0fdf4; color: var(--accent); }}

        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}
        .section-title {{ font-size: 1.15rem; font-weight: 700; margin: 25px 0 15px 0; display: flex; align-items: center; justify-content: space-between; }}
        
        /* Сетка карточек в стиле APKPure */
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 15px; }}
        .card {{ background: var(--card-bg); border-radius: 14px; padding: 16px; text-decoration: none; color: inherit; display: flex; flex-direction: column; align-items: center; text-align: center; border: 1px solid var(--border); transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-color: var(--accent); }}
        
        .app-icon {{ width: 72px; height: 72px; border-radius: 16px; object-fit: cover; margin-bottom: 12px; background: #eee; box-shadow: 0 4px 10px rgba(0,0,0,0.06); }}
        .app-name {{ font-size: 0.92rem; font-weight: 600; margin-bottom: 4px; color: var(--text); display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; width: 100%; }}
        .app-cat {{ font-size: 0.75rem; color: var(--text-light); margin-bottom: 10px; }}
        .app-meta {{ font-size: 0.75rem; color: var(--accent); font-weight: 700; background: #f0fdf4; padding: 4px 10px; border-radius: 20px; width: 100%; box-sizing: border-box; }}
        
        .overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); display: none; z-index: 999; }}
        .overlay.active {{ display: block; }}
    </style>
</head>
<body>

    <header>
        <div class="header-left">
            <button class="burger" onclick="toggleMenu()">☰</button>
            <a href="index.html" class="logo">APK<span>Pure</span></a>
        </div>
        <div class="search-container">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="Поиск приложений (happ, v2rayng, nekobox...)" onkeyup="filterApps()">
        </div>
        <div style="width: 24px;"></div>
    </header>

    <div class="overlay" id="overlay" onclick="toggleMenu()"></div>
    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <span>Категории</span>
            <button class="close-btn" onclick="toggleMenu()">✕</button>
        </div>
        <a href="index.html" class="cat-item">🏠 Все приложения</a>
"""

    for cat in categories:
        index_html += f'        <a href="index.html?cat={urllib_quote(cat)}" class="cat-item">📂 {cat}</a>\n'

    index_html += """
    </div>

    <div class="container">
        <div class="section-title">🔥 Топ-50 скачиваемых APK</div>
        <div class="grid" id="appGrid">
"""

    for app in apps[:50]:
        slug = app.get("slug", "")
        name = app.get("name", "App")
        category = app.get("category", "Утилиты")
        size = app.get("file_size", "15 MB")
        icon = get_smart_icon(app)
        
        index_html += f"""
            <a href="{slug}.html" class="card" data-name="{name.lower()}" data-cat="{category.lower()}">
                <img src="{icon}" class="app-icon" alt="{name}">
                <div class="app-name">{name}</div>
                <div class="app-cat">{category}</div>
                <div class="app-meta">{size}</div>
            </a>
"""

    index_html += """
        </div>
    </div>

    <script>
        function toggleMenu() {
            document.getElementById('sidebar').classList.toggle('open');
            document.getElementById('overlay').classList.toggle('active');
        }

        function filterApps() {
            let query = document.getElementById('searchInput').value.toLowerCase();
            let cards = document.getElementsByClassName('card');
            for (let card of cards) {
                let name = card.getAttribute('data-name');
                let cat = card.getAttribute('data-cat');
                if (name.includes(query) || cat.includes(query)) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            }
        }
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Генерация страниц приложений в том же чистом стиле
    for app in apps:
        slug = app.get("slug", "")
        name = app.get("name", "App")
        category = app.get("category", "Утилиты")
        rating = app.get("rating", "4.8")
        size = app.get("file_size", "15 MB")
        date = app.get("date", "14.10.2026")
        fallback = app.get("fallback_apk", "#")
        desc = app.get("desc", "")
        icon = get_smart_icon(app)

        app_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — Скачать APK бесплатно</title>
    <style>
        body {{ background: #f5f6f7; color: #222; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .container {{ background: #ffffff; border-radius: 20px; padding: 30px; max-width: 480px; width: 100%; border: 1px solid #e6e6e6; box-shadow: 0 10px 25px rgba(0,0,0,0.04); }}
        .header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }}
        .app-icon {{ width: 84px; height: 84px; border-radius: 20px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        h1 {{ margin: 0 0 6px 0; font-size: 1.35rem; color: #222; }}
        .cat {{ color: #777; font-size: 0.9rem; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; background: #f8f9fa; padding: 14px; border-radius: 12px; font-size: 0.9rem; }}
        .desc {{ margin: 20px 0; color: #444; line-height: 1.6; font-size: 0.95rem; }}
        .btn {{ display: block; background: #00ce84; color: white; text-align: center; padding: 14px; border-radius: 14px; text-decoration: none; font-weight: bold; margin-top: 20px; transition: 0.2s; box-shadow: 0 4px 14px rgba(0,206,132,0.3); font-size: 1rem; }}
        .btn:hover {{ background: #00b372; }}
        .back {{ display: block; text-align: center; margin-top: 15px; color: #777; text-decoration: none; font-size: 0.9rem; }}
        .back:hover {{ color: #222; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="{icon}" class="app-icon" alt="{name}">
            <div>
                <h1>{name}</h1>
                <div class="cat">📂 {category}</div>
            </div>
        </div>
        <div class="info-grid">
            <div>⭐ Рейтинг: <b>{rating}</b></div>
            <div>💾 Размер: <b>{size}</b></div>
            <div style="grid-column: span 2;">📅 Обновлено: <b>{date}</b></div>
        </div>
        <div class="desc">{desc}</div>
        <a href="{fallback}" class="btn" target="_blank">📥 Скачать APK (Прямая ссылка)</a>
        <a href="index.html" class="back">← На главную каталог</a>
    </div>
</body>
</html>
"""
        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(app_html)

    print("APKPure style generated!")

if __name__ == "__main__":
    generate()
