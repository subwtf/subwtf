import time
import os
import json
import urllib.request
import urllib.error
import re

REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")
TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
CHANNEL_ID = "@semenkicha"

def log(msg):
    print(f"[NATIVE-DAEMON] {msg}")
    with open(os.path.join(REPO_PATH, "daemon.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def parse_4pda_native(url):
    """Парсинг 4PDA с помощью встроенных модулей Python"""
    apps = []
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Извлекаем заголовок темы через регулярное выражение
            match_title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
            title = "4PDA Release"
            if match_title:
                title = re.sub(r'<.*?>', '', match_title.group(1)).strip()

            # Ищем ссылки на скачивание APK в теме
            links = re.findall(r'href="(https?://[^"]+?\.(?:apk|zip))"', html)
            dl_link = links[0] if links else url

            apps.append({
                "name": title[:50],
                "category": "4PDA Релизы",
                "rating": "4.9",
                "file_size": "25+ MB",
                "fallback_apk": dl_link,
                "desc": f"Проверенный релиз с форума 4PDA: {title}"
            })
    except Exception as e:
        log(f"Ошибка парсинга 4PDA: {e}")
    return apps

def fetch_github_native():
    """Сбор софта с GitHub через встроенный urllib"""
    new_apps = []
    queries = ["android apk player", "smarttv launcher apk", "iptv client android", "emulator android app"]
    for q in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={q.replace(' ', '+')}+extension:apk&sort=updated&per_page=10"
            req = urllib.request.Request(url, headers={"User-Agent": "Python-Client", "Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for item in data.get("items", []):
                    new_apps.append({
                        "name": item.get("name"),
                        "category": "Утилиты с GitHub",
                        "rating": "4.8",
                        "file_size": "20 MB",
                        "fallback_apk": item.get("html_url") + "/releases",
                        "desc": (item.get("description") or "GitHub APK")[:300]
                    })
            time.sleep(1)
        except:
            pass
    return new_apps

def job():
    log("Штурм 4PDA и GitHub...")
    
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"apps": [], "archive": []}

    apps = data.get("apps", [])
    archive = data.get("archive", [])
    
    # Парсим 4PDA и GitHub
    target_url = "https://4pda.to/forum/index.php?showtopic=939554"
    p4 = parse_4pda_native(target_url)
    gh = fetch_github_native()
    
    all_found = p4 + gh
    existing_names = {a.get("name") for a in apps + archive if isinstance(a, dict)}
    added = 0

    for app in all_found:
        if app["name"] not in existing_names:
            apps.append(app)
            existing_names.add(app["name"])
            added += 1

    log(f"Добавлено новых релизов: {added}. Всего в базе: {len(apps)}")

    data["apps"] = apps
    data["archive"] = archive
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Пересобираем сайт
    os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")

    # Публикуем в Telegram-канал
    if apps:
        app = apps.pop(0)
        name = app.get('name', 'App')
        cat = app.get('category', 'Утилиты')
        size = app.get('file_size', 'N/A')
        desc = app.get('desc', 'Описание отсутствует.')[:200]
        link = app.get('fallback_apk', 'https://4pda.to')
        
        text = (
            f"🔥 **Новый релиз:** *{name}*\n"
            f"📂 Категория: {cat} | 📦 Размер: {size}\n\n"
            f"📝 {desc}...\n\n"
            f"🔗 Скачать / Источник: {link}\n"
            f"👉 Каталог: https://subwtf.github.io/subwtf/"
        )
        
        try:
            req_data = json.dumps({"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}).encode('utf-8')
            req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=req_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    archive.append(app)
                    data["apps"] = apps
                    data["archive"] = archive
                    with open(DB_PATH, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    log(f"Опубликовано в канал: {name}")
        except Exception as e:
            log(f"Ошибка публикации: {e}")

    # Синхронизация с GitHub
    os.system(f"cd {REPO_PATH} && git add . && git commit -m 'Native parser sync' && git push origin main")

def main():
    log("Нативный демон-парсер запущен 24/7.")
    while True:
        try:
            job()
        except Exception as e:
            log(f"Ошибка: {e}")
        time.sleep(600)

if __name__ == "__main__":
    main()
