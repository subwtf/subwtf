import json, os, urllib.request, urllib.parse, random, re, time
from datetime import datetime

TOKEN = "8794166379:AAHNKSewwvQi2XYPLdV2rUKLz2ZmPl6UCgQ"
ADMIN_ID = 5199807862
CHANNEL = "@semenkicha"
DB_FILE = "database.json"
SITE_URL = "https://subwtf.github.io/subwtf"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "sources" not in data: data["sources"] = []
            return data
    return {"apps": [], "sent": [], "total_scraped": 0, "sources": []}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def parse_github_with_progress(chat_id):
    db = load_db()
    existing_slugs = {app["slug"] for app in db["apps"]}
    queries = ["android apk", "smarttv apk", "iptv player", "media center android"]
    if chat_id:
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": chat_id, "text": "⚡ Турбо-парсер запущен...", "parse_mode": "HTML"}).encode())
    new_apps = []
    total_checked = 0
    for q in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=updated&per_page=20"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                items = json.loads(resp.read().decode()).get("items", [])
                total_checked += len(items)
                for item in items:
                    name = item.get("name")
                    slug = re.sub(r"[^a-zA-Z0-9]", "-", name).lower().strip("-")
                    if not slug or len(slug) < 2 or slug in existing_slugs: continue
                    existing_slugs.add(slug)
                    new_apps.append({
                        "slug": slug, "name": name, "category": "Smart TV",
                        "rating": "4.8", "icon": "🚀", "file_size": "15.4 MB",
                        "date": datetime.now().strftime("%d.%m.%Y"),
                        "fallback_apk": f"{item.get('html_url')}/releases",
                        "desc": (item.get("description") or "APK из репозитория.")[:140]
                    })
        except: pass
    if new_apps:
        db["apps"].extend(new_apps)
        db["total_scraped"] += len(new_apps)
        save_db(db)
        os.system("cd /root/subwtf-repo && python3 generator.py && git add . && git commit -m 'Turbo update' && git push origin main > /dev/null 2>&1")
    if chat_id:
        report = f"✅ Готово! Проверено: {total_checked}, добавлено: {len(new_apps)}"
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": chat_id, "text": report}).encode())

def main_loop():
    print("Бот запущен...")
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=10"
            with urllib.request.urlopen(url, timeout=15) as resp:
                for r in json.loads(resp.read().decode()).get("result", []):
                    offset = r["update_id"] + 1
                    if "message" in r and r["message"].get("chat", {}).get("id") == ADMIN_ID:
                        text = r["message"].get("text", "")
                        chat_id = r["message"]["chat"]["id"]
                        if text == "/start":
                            kb = json.dumps({"keyboard": [[{"text": "🔄 Запустить парсинг сейчас"}, {"text": "📊 Статус"}], [{"text": "🗑 Сбросить историю"}]], "resize_keyboard": True})
                            urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": chat_id, "text": "Панель управления Git App WTF 🤨", "reply_markup": kb}).encode())
                        elif text == "🔄 Запустить парсинг сейчас":
                            parse_github_with_progress(chat_id)
        except: time.sleep(3)

if __name__ == "__main__":
    main_loop()
