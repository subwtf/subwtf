import time
import os
import json
import requests

REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")
TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
CHANNEL_ID = "@semenkicha"

def log(msg):
    print(f"[DAEMON SCANNER] {msg}")
    with open(os.path.join(REPO_PATH, "daemon.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def fetch_github_apks():
    """Поиск новых приложений с APK через GitHub API"""
    new_apps = []
    try:
        # Ищем репозитории с андроид приложениями и APK в релизах
        url = "https://api.github.com/search/repositories?q=android+apk+extension:apk&sort=updated&per_page=10"
        headers = {"Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            items = res.json().get("items", [])
            for item in items:
                name = item.get("name")
                desc = item.get("description") or "Описание отсутствует."
                html_url = item.get("html_url")
                
                # Формируем объект приложения
                app = {
                    "name": name,
                    "category": "Утилиты с GitHub",
                    "rating": "4.8",
                    "file_size": "20+ MB",
                    "fallback_apk": html_url + "/releases",
                    "desc": desc[:300]
                }
                new_apps.append(app)
    except Exception as e:
        log(f"Ошибка при запросе к GitHub API: {e}")
    return new_apps

def job():
    log("Сканирование GitHub в поисках новых релизов...")
    
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"apps": [], "archive": []}

    apps = data.get("apps", [])
    archive = data.get("archive", [])
    
    # Получаем свежие находки с GitHub
    scanned_apps = fetch_github_apks()
    
    added_count = 0
    existing_names = {a.get("name") for a in apps + archive if isinstance(a, dict)}

    for app in scanned_apps:
        if app["name"] not in existing_names:
            apps.append(app)
            existing_names.add(app["name"])
            added_count += 1

    log(f"Найдено и добавлено новых приложений: {added_count}")

    data["apps"] = apps
    data["archive"] = archive
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Пересобираем сайт
    os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")

    # Публикуем свежее приложение в Telegram-канал, если есть очередь
    if apps:
        app = apps.pop(0)
        name = app.get('name', 'App')
        cat = app.get('category', 'Утилиты')
        size = app.get('file_size', 'N/A')
        desc = app.get('desc', 'Описание отсутствует.')[:200]
        link = app.get('fallback_apk', 'https://github.com')
        
        text = (
            f"🔥 **Новый релиз с GitHub:** *{name}*\n"
            f"📂 Категория: {cat} | 📦 Размер: {size}\n\n"
            f"📝 {desc}...\n\n"
            f"🔗 Репозиторий: {link}\n"
            f"👉 Каталог: https://subwtf.github.io/subwtf/"
        )
        
        res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
        if res.status_code == 200:
            archive.append(app)
            data["apps"] = apps
            data["archive"] = archive
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            log(f"Успешно опубликовано в канал: {name}")

    # Синхронизация с GitHub
    os.system(f"cd {REPO_PATH} && git add . && git commit -m 'Auto daemon: parser sync' && git push origin main")

def main():
    log("Полноценный демон-парсер запущен 24/7.")
    while True:
        try:
            job()
        except Exception as e:
            log(f"Ошибка в цикле: {e}")
        # Пауза 15 минут перед следующим штурмом GitHub
        time.sleep(900)

if __name__ == "__main__":
    main()
