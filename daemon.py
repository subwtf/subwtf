import time, os, json, urllib.request, re
REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")
TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
CHANNEL_ID = "@semenkicha"

def log(msg):
    print(f"[DAEMON] {msg}")
    with open(os.path.join(REPO_PATH, "daemon.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def job():
    log("Штурм GitHub и обновление каталога...")
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"apps": [], "archive": []}
    
    apps = data.get("apps", [])
    archive = data.get("archive", [])
    
    # Сбор с GitHub
    try:
        url = "https://api.github.com/search/repositories?q=android+apk+extension:apk&sort=updated&per_page=15"
        req = urllib.request.Request(url, headers={"User-Agent": "Python", "Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            items = json.loads(resp.read().decode("utf-8")).get("items", [])
            existing = {a.get("name") for a in apps + archive if isinstance(a, dict)}
            added = 0
            for item in items:
                name = item.get("name")
                if name and name not in existing:
                    apps.append({
                        "name": name,
                        "category": "GitHub Релизы",
                        "rating": "4.8",
                        "file_size": "20 MB",
                        "fallback_apk": item.get("html_url") + "/releases",
                        "desc": (item.get("description") or "APK с GitHub")[:300]
                    })
                    existing.add(name)
                    added += 1
            log(f"Добавлено новых: {added}")
    except Exception as e:
        log(f"Ошибка GitHub: {e}")

    data["apps"] = apps
    data["archive"] = archive
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")

    if apps:
        app = apps.pop(0)
        name = app.get("name", "App")
        text = f"🔥 **Новый релиз:** *{name}*\n👉 Каталог: https://subwtf.github.io/subwtf/"
        try:
            req_data = json.dumps({"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}).encode("utf-8")
            req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10):
                archive.append(app)
                data["apps"] = apps
                data["archive"] = archive
                with open(DB_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                log(f"Опубликовано: {name}")
        except Exception as e:
            log(f"Ошибка отправки: {e}")

    os.system(f"cd {REPO_PATH} && git add . && git commit -m 'Auto sync' && git push origin main")

if __name__ == "__main__":
    while True:
        try:
            job()
        except Exception as e:
            log(f"Ошибка цикла: {e}")
        time.sleep(600)
