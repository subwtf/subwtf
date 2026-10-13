import json, os

DB_FILE = "database.json"

def generate():
    if not os.path.exists(DB_FILE):
        print("Database not found!")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    apps = db.get("apps", [])
    
    # Собираем категории для меню
    categories = sorted(list(set(app.get("category", "Утилиты") for app in apps)))

    # Генерация главной страницы в стиле APKPure (светлая тема, иконки, бургер, топ)
    index_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git App WTF — Каталог APK приложений</title>
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-secondary: #64748b;
            --accent: #10b981;
            --accent-hover: #059669;
            --border: #e2e8f0;
        }}
        body {{ background: var(--bg-color); color: var(--text-main); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; }}
        header {{ background: #ffffff; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; }}
        .logo {{ font-size: 1.25rem; font-weight: bold; color: #0f172a; text-decoration: none; display: flex; align-items: center; gap: 8px; }}
        .logo span {{ color: var(--accent); }}
        .burger {{ background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-main); }}
        
        /* Боковое меню */
        .sidebar {{ position: fixed; top: 0; left: -280px; width: 280px; height: 100%; background: #ffffff; box-shadow: 4px 0 15px rgba(0,0,0,0.1); z-index: 1000; transition: 0.3s ease; padding: 20px; box-sizing: border-box; overflow-y: auto; }}
        .sidebar.open {{ left: 0; }}
        .sidebar-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 1.1rem; font-weight: bold; }}
        .close-btn {{ background: none; border: none; font-size: 1.2rem; cursor: pointer; }}
        .cat-item {{ display: block; padding: 10px 15px; color: var(--text-main); text-decoration: none; border-radius: 8px; margin-bottom: 5px; transition: 0.2s; font-weight: 500; }}
        .cat-item:hover {{ background: #f1f5f9; color: var(--accent); }}

        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}
        h2 {{ font-size: 1.2rem; margin-bottom: 15px; color: var(--text-main); border-left: 4px solid var(--accent); padding-left: 10px; }}
        
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .card {{ background: var(--card-bg); border-radius: 14px; padding: 15px; text-decoration: none; color: inherit; display: flex; flex-direction: column; align-items: center; text-align: center; border: 1px solid var(--border); box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: 0.2s; }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.06); border-color: var(--accent); }}
        
        .app-icon {{ width: 68px; height: 68px; border-radius: 16px; object-fit: cover; margin-bottom: 10px; background: #e2e8f0; }}
        .app-name {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; color: var(--text-main); display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; width: 100%; }}
        .app-cat {{ font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 8px; }}
        .app-meta {{ font-size: 0.75rem; color: var(--accent); font-weight: 600; background: #ecfdf5; padding: 2px 8px; border-radius: 6px; }}
        
        .overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); display: none; z-index: 999; }}
        .overlay.active {{ display: block; }}
    </style>
</head>
<body>

    <header>
        <button class="burger" onclick="toggleMenu()">☰</button>
        <a href="index.html" class="logo">Git App <span>WTF</span></a>
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
        index_html += f'        <a href="#cat-{cat}" class="cat-item" onclick="toggleMenu()">📂 {cat}</a>\n'

    index_html += """
    </div>

    <div class="container">
        <h2>🔥 Топ скачиваемых APK (Топ-50)</h2>
        <div class="grid">
"""

    # Выводим до 50 популярных приложений
    for app in apps[:50]:
        slug = app.get("slug", "")
        name = app.get("name", "App")
        category = app.get("category", "Утилиты")
        size = app.get("file_size", "15 MB")
        icon = app.get("icon_url", "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        
        index_html += f"""
            <a href="{slug}.html" class="card">
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
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Генерация детальных страниц приложений
    for app in apps:
        slug = app.get("slug", "")
        name = app.get("name", "App")
        category = app.get("category", "Утилиты")
        rating = app.get("rating", "4.8")
        size = app.get("file_size", "15 MB")
        date = app.get("date", "14.10.2026")
        fallback = app.get("fallback_apk", "#")
        desc = app.get("desc", "")
        icon = app.get("icon_url", "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")

        app_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — Скачать APK</title>
    <style>
        body {{ background: #f8fafc; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .container {{ background: #ffffff; border-radius: 20px; padding: 25px; max-width: 480px; width: 100%; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
        .header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
        .app-icon {{ width: 80px; height: 80px; border-radius: 18px; object-fit: cover; background: #e2e8f0; }}
        h1 {{ margin: 0 0 5px 0; font-size: 1.3rem; color: #0f172a; }}
        .cat {{ color: #64748b; font-size: 0.9rem; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; background: #f8fafc; padding: 12px; border-radius: 12px; font-size: 0.9rem; }}
        .desc {{ margin: 20px 0; color: #334155; line-height: 1.6; font-size: 0.95rem; }}
        .btn {{ display: block; background: #10b981; color: white; text-align: center; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: bold; margin-top: 20px; transition: 0.2s; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }}
        .btn:hover {{ background: #059669; }}
        .back {{ display: block; text-align: center; margin-top: 15px; color: #64748b; text-decoration: none; font-size: 0.9rem; }}
        .back:hover {{ color: #0f172a; }}
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
        <a href="index.html" class="back">← Вернуться в каталог</a>
    </div>
</body>
</html>
"""
        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(app_html)

    print("Сайт успешно пересобран в стиле APKPure!")

if __name__ == "__main__":
    generate()
