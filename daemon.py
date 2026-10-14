import time
import os
import json
import requests

REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")
TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
CHANNEL_ID = "@semenkicha"

def log(msg):
    print(f"[MEGA-DAEMON] {msg}")
    with open(os.path.join(REPO_PATH, "daemon.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def fetch_massive_apks():
    """Масштабный поиск сотен APK-приложений по множеству категорий на GitHub"""
    queries = [
        "android apk player", "smarttv launcher apk", "iptv client android",
        "emulator android app", "proxy vpn client apk", "tools utility android",
        "media player android", "open source android app", "github android release",
        "downloader manager apk", "browser security android", "game client apk"
    ]
    
    new_apps = []
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    for q in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={q}+extension:apk&sort=updated&per_page=30"
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                items = res.json().get("items", [])
                for item in items:
                    name = item.get("name")
                    desc = item.get("description") or "Современное приложение с открытым исходным кодом."
                    html_url = item.get("html_url")
                    
                    # Автоматическое определение категории по ключевым словам
                    q_lower = q.lower()
                    if "tv" in q_lower or "player" in q_lower:
                        category = "Smart TV / Медиа"
                    elif "emulator" in q_lower or "game" in q_lower:
                        category = "Игры / Эмуляторы"
                    elif "proxy" in q_lower or "vpn" in q_lower or "browser" in q_lower:
                        category = "Сеть и Proxy"
                    else:
                        category = "Системные / Утилиты"

                    app = {
                        "name": name,
                        "category": category,
                        "rating": "4.8",
                        "file_size": "15-45 MB",
                        "fallback_apk": html_url + "/releases",
                        "desc": desc[:300]
                    }
                    new_apps.append(app)
            time.sleep(2) # Пауза между поисковыми запросами во избежание лимитов GitHub
        except Exception as e:
            log(f"Ошибка при запросе {q}: {e}")
            
    return new_apps

def job():
    log("Запуск масштабного штурма GitHub для сбора сотен приложений...")
    
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"apps": [], "archive": []}

    apps = data.get("apps", [])
    archive = data.get("archive", [])
    
    # Собираем свежие сокровища
    scanned = fetch_massive_apks()
    
    existing_names = {a.get("name") for a in apps + archive if isinstance(a, dict)}
    added = 0

    for app in scanned:
        if app["name"] not in existing_names:
            apps.append(app)
            existing_names.add(app["name"])
            added += 1

    log(f"Добавлено новых приложений в копилку: {added}. Всего в базе: {len(apps)}")

    data["apps"] = apps
    data["archive"] = archive
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 1. Пересобираем сайт со всеми новыми приложениями
    os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")

    # 2. Публикуем релиз в Telegram-канал (если есть в очереди)
    if apps:
        app = apps.pop(0)
        name = app.get('name', 'App')
        cat = app.get('category', 'Утилиты')
        size = app.get('file_size', 'N/A')
        desc = app.get('desc', 'Описание отсутствует.')[:200]
        link = app.get('fallback_apk', 'https://github.com')
        
        text = (
            f"🔥 **Новый релиз в каталоге:** *{name}*\n"
            f"📂 Категория: {cat} | 📦 Размер: {size}\n\n"
            f"📝 {desc}...\n\n"
            f"🔗 Репозиторий: {link}\n"
            f"👉 Скачать в каталоге: https://subwtf.github.io/subwtf/"
        )
        
        res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
        if res.status_code == 200:
            archive.append(app)
            data["apps"] = apps
            data["archive"] = archive
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            log(f"Успешно опубликовано в канал: {name}")

    # 3. Синхронизируем изменения с GitHub-репозиторием сайта
    os.system(f"cd {REPO_PATH} && git add . && git commit -m 'Mega-daemon: massive sync' && git push origin main")

def main():
    log("Мега-демон запущен 24/7 на полную мощность.")
    while True:
        try:
            job()
        except Exception as e:
            log(f"Ошибка в цикле: {e}")
        
        # Цикл проверки каждые 10 минут, чтобы постоянно подтягивать новые сотни приложений
        time.sleep(600)

if __name__ == "__main__":
    main()
