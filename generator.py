import json, os, urllib.request, urllib.parse, re, random
from datetime import datetime

REF_LINK = "https://iseetv.net/welcome/signup/cb26f9e15332cb38"

DB_FILE = "database.json"
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        APPS = data.get("apps", [])
else:
    APPS = [
        {"slug": "televizo", "name": "Televizo", "category": "IPTV Плееры", "rating": "4.9", "icon": "📺", "file_size": "18.4 MB", "date": "12.10.2026", "fallback_apk": "#", "desc": "Мощный IPTV плеер для Android TV."},
        {"slug": "smarttube", "name": "SmartTube", "category": "Smart TV", "rating": "5.0", "icon": "🔴", "file_size": "24.1 MB", "date": "13.10.2026", "fallback_apk": "#", "desc": "YouTube клиент без рекламы."}
    ]

LIGHT_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f8; color: #222; line-height: 1.4; }
a { text-decoration: none; color: inherit; }
header { background: #ffffff; border-bottom: 1px solid #e1e4e8; padding: 0.75rem 1rem; position: sticky; top: 0; z-index: 10; display: flex; align-items: center; justify-content: space-between; }
.logo { font-size: 1.1rem; font-weight: 700; color: #111; display: flex; align-items: center; gap: 0.4rem; }
.logo span { color: #2563eb; }
.search { background: #f1f3f5; border: 1px solid #dcdfe6; border-radius: 6px; padding: 0.4rem 0.75rem; font-size: 0.85rem; width: 45%; max-width: 250px; outline: none; }
.container { max-width: 900px; margin: 0 auto; padding: 0.75rem; }
.banner { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; }
.banner h3 { font-size: 0.95rem; color: #1e3a8a; margin-bottom: 0.25srem; }
.banner p { font-size: 0.75rem; color: #475569; margin-bottom: 0.5rem; }
.banner a { display: inline-block; background: #2563eb; color: #fff; padding: 0.4rem 0.75rem; border-radius: 5px; font-size: 0.75rem; font-weight: 600; }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem; }
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.65rem; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
.card-top { display: flex; gap: 0.5rem; align-items: flex-start; }
.icon { width: 2.5rem; height: 2.5rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; flex-shrink: 0; }
.title { font-size: 0.85rem; font-weight: 700; color: #1a202c; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cat { font-size: 0.65rem; color: #64748b; font-weight: 600; }
.desc { font-size: 0.7rem; color: #475569; margin: 0.4rem 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.meta { display: flex; justify-content: space-between; font-size: 0.6rem; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 0.35rem; }
footer { text-align: center; padding: 1.5rem; font-size: 0.75rem; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 1.5rem; background: #fff; }
"""

cards_html = ""
for app in APPS:
    cards_html += f"""
    <a href="{app[slug]}.html" class="card">
        <div>
            <div class="card-top">
                <div class="icon">{app.get(icon, 📦)}</div>
                <div style="min-width: 0; flex-grow: 1;">
                    <div class="title">{app[name]}</div>
                    <div class="cat">{app[category]} &bull; ★ {app[rating]}</div>
                </div>
            </div>
            <div class="desc">{app[desc]}</div>
        </div>
        <div class="meta"><span>💾 {app[file_size]}</span><span>📅 {app[date]}</span></div>
    </a>
    """

index_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git App WTF 🤨 — Скачать APK</title>
    <style>{LIGHT_CSS}</style>
</head>
<body>
    <header>
        <a href="index.html" class="logo">🤨 Git App <span>WTF</span></a>
        <input type="text" class="search" placeholder="Поиск APK...">
    </header>
    <main class="container">
        <div class="banner">
            <h3>🔥 Партнерский IPTV Плейлист</h3>
            <p>1000+ каналов в HD/4K качестве.</p>
            <a href="{REF_LINK}" target="_blank">Получить тест &rarr;</a>
        </div>
        <div class="grid">{cards_html}</div>
    </main>
    <footer>&copy; 2026 Git App WTF 🤨 — Каталог APK</footer>
</body>
</html>"""

open("index.html", "w", encoding="utf-8").write(index_html)

for app in APPS:
    app_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Скачать {app[name]} APK — Git App WTF</title>
    <style>{LIGHT_CSS}</style>
</head>
<body>
    <header>
        <a href="index.html" class="logo">🤨 Git App <span>WTF</span></a>
    </header>
    <main class="container" style="max-width: 600px;">
        <a href="index.html" style="color: #2563eb; font-size: 0.75rem; font-weight: 600; display: inline-block; margin-bottom: 0.75rem;">&larr; На главную</a>
        <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; display: flex; gap: 0.75rem; align-items: center;">
            <div style="font-size: 2.5rem;">{app.get(icon, 📦)}</div>
            <div>
                <h1 style="font-size: 1.15rem; font-weight: 700; color: #111;">{app[name]}</h1>
                <div style="font-size: 0.7rem; color: #64748b;">★ {app[rating]} &bull; {app[category]} &bull; 💾 {app[file_size]} &bull; 📅 {app[date]}</div>
            </div>
        </div>
        <div style="margin-bottom: 1rem;">
            <a href="{app[fallback_apk]}" style="background: #2563eb; color: #fff; display: block; text-align: center; padding: 0.75rem; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">📥 Скачать APK файл ({app[file_size]})</a>
        </div>
        <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem;">
            <h2 style="font-size: 0.9rem; font-weight: 700; margin-bottom: 0.4rem;">Описание</h2>
            <p style="font-size: 0.75rem; color: #475569;">{app[desc]}</p>
        </div>
    </main>
    <footer>&copy; 2026 Git App WTF 🤨</footer>
</body>
</html>"""
    open(f"{app[slug]}.html", "w", encoding="utf-8").write(app_html)

print("Генерация завершена успешно!")
