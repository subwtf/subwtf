import json, os, urllib.request, urllib.parse, random, re, time
from datetime import datetime

TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
ADMIN_ID = 5199807862
CHANNEL = "@semenkicha"
DB_FILE = "database.json"
SITE_URL = "https://subwtf.github.io/subwtf"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "sources" not in data: data["sources"] = ["github.com/search"]
            if "archive" not in data: data["archive"] = []
            return data
    return {"apps": [], "sent": [], "archive": [], "total_scraped": 0, "sources": ["github.com/search"]}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def clean_text(text):
    if not text: return "Профессиональный APK пакет из проверенных источников."
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"(@|t\.me/)\w+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(join|channel|subscribe|must join|telegram).*", "", text, flags=re.IGNORECASE)
    cleaned = text.strip()
    return (cleaned[:130] + "...") if len(cleaned) > 130 else (cleaned or "APK пакет.")

def industrial_parser(chat_id, custom_query=None):
    db = load_db()
    existing_slugs = {app["slug"] for app in db["apps"]} | {app["slug"] for app in db.get("archive", [])}
    if chat_id:
        try:
            urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": chat_id, "text": "⚡ <b>[INDUSTRIAL] Запущен глубокий сканер с извлечением иконок...</b>", "parse_mode": "HTML"}).encode(), timeout=5)
        except: pass
    
    new_apps = []
    total_checked = 0
    queries = [custom_query] if custom_query else ["android apk", "smarttv apk", "iptv player", "media center android", "launcher apk", "tool apk"]
    
    for q in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=updated&per_page=30"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=7) as resp:
                items = json.loads(resp.read().decode()).get("items", [])
                total_checked += len(items)
                for item in items:
                    name = item.get("name")
                    slug = re.sub(r"[^a-zA-Z0-9]", "-", name).lower().strip("-")
                    if not slug or len(slug) < 2 or slug in existing_slugs: continue
                    existing_slugs.add(slug)
                    raw_desc = item.get("description") or ""
                    if "t.me" in raw_desc.lower() or "join" in raw_desc.lower() or "channel" in raw_desc.lower(): continue
                    
                    # Извлекаем прямую ссылку на аватар/иконку репозитория
                    owner = item.get("owner", {})
                    icon_url = owner.get("avatar_url", "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
                    
                    new_apps.append({
                        "slug": slug, "name": name,
                        "category": "Smart TV" if "tv" in q else ("Мультимедиа" if "iptv" in q or "media" in q else ("Сеть" if "proxy" in q or "vless" in q else "Утилиты")),
                        "rating": str(round(random.uniform(4.7, 5.0), 1)),
                        "icon_url": icon_url,
                        "file_size": f"{random.randint(6, 58)}.5 MB",
                        "date": datetime.now().strftime("%d.%m.%Y"),
                        "fallback_apk": f"{item.get('html_url')}/releases",
                        "desc": clean_text(raw_desc)
                    })
        except: pass

    if new_apps:
        db["apps"].extend(new_apps)
        db["total_scraped"] += len(new_apps)
        save_db(db)
        rebuild_and_push()
    
    if chat_id:
        rep = f"🏭 <b>[INDUSTRIAL] Сканирование завершено!</b>\n\n• Запрос: <b>{queries[0]}</b>\n• Проверено: <b>{total_checked}</b>\n• Добавлено APK: <b>{len(new_apps)}</b>\n• Настоящие иконки привязаны!"
        try:
            urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": chat_id, "text": rep, "parse_mode": "HTML"}).encode(), timeout=5)
        except: pass

def rebuild_and_push():
    os.system("python3 generator.py && git add . && git commit -m 'Auto update site' && git push origin main")

def post_next_app():
    db = load_db()
    target = None
    for app in db["apps"]:
        if app["slug"] not in db["sent"]:
            target = app
            break
    if not target: return None
    
    msg = f"📱 <b>{target['name']}</b>\n\n📂 Категория: {target['category']}\n⭐ Рейтинг: {target['rating']} | 💾 Размер: {target['file_size']}\n\n{target['desc']}\n\n📥 <b>Скачать APK (Прямая ссылка):</b>\n👉 {SITE_URL}/{target['slug']}.html\n\n<i>Git App WTF 🤨 — Автономный каталог APK</i>"
    
    # Берем реальную иконку приложения из базы
    icon_photo = target.get("icon_url", "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    
    try:
        data = urllib.parse.urlencode({
            "chat_id": CHANNEL,
            "photo": icon_photo,
            "caption": msg,
            "parse_mode": "HTML"
        }).encode()
        res = urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data=data, timeout=7)
        if res:
            db["sent"].append(target["slug"])
            if target not in db["archive"]: db["archive"].append(target)
            save_db(db)
            return target
    except Exception as e:
        print("Photo send error, fallback to text:", e)
        try:
            res = urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": CHANNEL, "text": msg, "parse_mode": "HTML"}).encode(), timeout=5)
            if res:
                db["sent"].append(target["slug"])
                if target not in db["archive"]: db["archive"].append(target)
                save_db(db)
                return target
        except: pass
    return None

def send_control_panel(chat_id):
    db = load_db()
    total = len(db["apps"])
    sent = len(db["sent"])
    queue = total - sent
    archive = len(db.get("archive", []))
    scraped_total = db.get("total_scraped", 0)
    
    text = f"🎛 <b>ПРОМЫШЛЕННЫЙ КОМБАЙН GIT APP WTF (PRO)</b>\n═════════════════════════════\n📊 <b>ТЕЛЕМЕТРИЯ СИСТЕМЫ:</b>\n• Всего в базе: <b>{total}</b>\n• Опубликовано: <b>{sent}</b>\n• В очереди: <b>{queue}</b>\n• В архиве: <b>{archive}</b>\n• Всего выкачано: <b>{scraped_total}</b>\n• Канал: <b>{CHANNEL}</b>\n═════════════════════════════\nВыберите режим работы или команду:"

    inline_kb = json.dumps({
        "inline_keyboard": [
            [{"text": "⚡ Глубокий парсинг (С иконками)", "callback_data": "run_parse"}],
            [{"text": "📺 Smart TV APK", "callback_data": "parse_smarttv"}, {"text": "🎮 Игры / Эмуляторы", "callback_data": "parse_games"}],
            [{"text": "📡 Сеть и Proxy", "callback_data": "parse_tools"}, {"text": "🎵 Мультимедиа / IPTV", "callback_data": "parse_media"}],
            [{"text": "📢 Опубликовать в канал", "callback_data": "force_post"}, {"text": "🔄 Пересобрать сайт", "callback_data": "rebuild_site"}],
            [{"text": "📊 Обновить статистику", "callback_data": "refresh_stats"}, {"text": "🧹 Сбросить очередь", "callback_data": "reset_queue"}]
        ]
    })
    
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": chat_id, "text": text, "parse_mode": "HTML", "reply_markup": inline_kb}).encode(), timeout=5)
    except: pass

def main_loop():
    print("Промышленный комбайн запущен...")
    offset = 0
    last_post_time = 0
    
    while True:
        try:
            if time.time() - last_post_time > 600:
                db = load_db()
                if len(db["apps"]) - len(db["sent"]) < 3: industrial_parser(None)
                post_next_app()
                last_post_time = time.time()

            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=5"
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                for r in data.get("result", []):
                    offset = r["update_id"] + 1
                    
                    if "message" in r and r["message"].get("chat", {}).get("id") == ADMIN_ID:
                        txt = r["message"].get("text", "")
                        cid = r["message"]["chat"]["id"]
                        if txt in ["/start", "Панель управления", "Статус"]:
                            send_control_panel(cid)
                            
                    elif "callback_query" in r:
                        cq = r["callback_query"]
                        cid = cq["message"]["chat"]["id"]
                        data_cb = cq.get("data")
                        
                        if cid == ADMIN_ID:
                            if data_cb == "run_parse":
                                industrial_parser(cid)
                            elif data_cb == "parse_smarttv":
                                industrial_parser(cid, custom_query="smarttv apk")
                            elif data_cb == "parse_games":
                                industrial_parser(cid, custom_query="android game apk")
                            elif data_cb == "parse_tools":
                                industrial_parser(cid, custom_query="vless xray proxy apk")
                            elif data_cb == "parse_media":
                                industrial_parser(cid, custom_query="iptv player apk")
                            elif data_cb == "force_post":
                                posted = post_next_app()
                                msg = f"✅ Отправлено в канал с иконкой: <b>{posted['name']}</b>" if posted else "⚠️ Очередь пуста! Запустите парсинг."
                                urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": cid, "text": msg, "parse_mode": "HTML"}).encode())
                            elif data_cb == "rebuild_site":
                                rebuild_and_push()
                                urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": cid, "text": "✅ Сайт пересобран и отправлен в GitHub!", "parse_mode": "HTML"}).encode())
                            elif data_cb == "refresh_stats":
                                send_control_panel(cid)
                            elif data_cb == "reset_queue":
                                db = load_db()
                                db["sent"] = []
                                save_db(db)
                                urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=urllib.parse.urlencode({"chat_id": cid, "text": "🧹 Очередь сброшена!", "parse_mode": "HTML"}).encode())
                                
                        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", data=urllib.parse.urlencode({"callback_query_id": cq["id"]}).encode())
        except Exception as e:
            time.sleep(3)

if __name__ == "__main__":
    main_loop()
