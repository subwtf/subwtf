import json, os

DB_FILE = "database.json"

def generate():
    if not os.path.exists(DB_FILE):
        print("Database not found!")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    apps = db.get("apps", [])

    # Генерация главной страницы (index.html)
    index_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git App WTF — Профессиональный каталог APK</title>
    <style>
        body {{ background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; }}
        h1 {{ text-align: center; color: #38bdf8; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 20px; text-decoration: none; color: inherit; display: block; border: 1px solid #334155; transition: 0.2s; }}
        .card:hover {{ border-color: #38bdf8; transform: translateY(-3px); }}
        .title {{ font-size: 1.2rem; font-weight: bold; margin-bottom: 8px; color: #f1f5f9; }}
        .cat {{ font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px; }}
        .desc {{ font-size: 0.9rem; color: #cbd5e1; }}
    </style>
</head>
<body>
    <h1>Git App WTF 🤨</h1>
    <div class="grid">
"""

    for app in apps:
        slug = app.get("slug", "")
        name = app.get("name", "App")
        category = app.get("category", "Утилиты")
        desc = app.get("desc", "")
        index_html += f"""
        <a href="{slug}.html" class="card">
            <div class="title">{name}</div>
            <div class="cat">📂 {category}</div>
            <div class="desc">{desc}</div>
        </a>
"""

    index_html += """
    </div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Генерация отдельных страниц для каждого приложения
    for app in apps:
        slug = app.get("slug", "")
        name = app.get("name", "App")
        category = app.get("category", "Утилиты")
        rating = app.get("rating", "5.0")
        size = app.get("file_size", "15 MB")
        date = app.get("date", "14.10.2026")
        fallback = app.get("fallback_apk", "#")
        desc = app.get("desc", "")

        app_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — Скачать APK</title>
    <style>
        body {{ background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .container {{ background: #1e293b; border-radius: 16px; padding: 30px; max-width: 500px; width: 100%; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
        h1 {{ margin-top: 0; color: #38bdf8; }}
        .info {{ margin: 15px 0; color: #94a3b8; font-size: 0.95rem; }}
        .desc {{ margin: 20px 0; color: #cbd5e1; line-height: 1.5; }}
        .btn {{ display: block; background: #0284c7; color: white; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 20px; transition: 0.2s; }}
        .btn:hover {{ background: #0369a1; }}
        .back {{ display: block; text-align: center; margin-top: 15px; color: #94a3b8; text-decoration: none; }}
        .back:hover {{ color: #f8fafc; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{name}</h1>
        <div class="info">📂 Категория: {category} | ⭐ Рейтинг: {rating}</div>
        <div class="info">💾 Размер: {size} | 📅 Обновлено: {date}</div>
        <div class="desc">{desc}</div>
        <a href="{fallback}" class="btn" target="_blank">📥 Скачать APK (Прямая ссылка)</a>
        <a href="index.html" class="back">← На главную каталог</a>
    </div>
</body>
</html>
"""
        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(app_html)

    print("Генерация завершена успешно!")

if __name__ == "__main__":
    generate()
