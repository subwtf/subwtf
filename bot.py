import time
import os
import json
import requests

TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
URL = f"https://api.telegram.org/bot{TOKEN}"
REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")

print("Бот запущен на чистом API...")

def get_updates(offset=None):
    params = {"timeout": 30, "offset": offset}
    try:
        response = requests.get(f"{URL}/getUpdates", params=params, timeout=35)
        return response.json().get("result", [])
    except Exception as e:
        print(f"Ошибка получения апдейтов: {e}")
        return []

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(f"{URL}/sendMessage", json=data)
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")

def get_keyboard():
    return {
        "keyboard": [
            [{"text": "📊 Состояние сервера"}, {"text": "📦 Приложений с GitHub"}],
            [{"text": "⏳ Очередь публикации"}, {"text": "⚡ Запустить сканирование GitHub"}]
        ],
        "resize_keyboard": True,
        "is_persistent": True
    }

def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if text == "/start":
        send_message(chat_id, "🛠 **Панель управления активирована.**\nВыберите нужный отчет или действие 👇", get_keyboard())
    
    elif text == "📊 Состояние сервера":
        disk = os.popen("df -h / | tail -1").read().split()
        cpu = os.popen("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").read().strip()
        ram = os.popen("free -m | grep Mem").read().split()
        uptime = os.popen("uptime -p").read().strip()
        
        rep = (
            f"🖥 **ОТЧЕТ: СОСТОЯНИЕ СЕРВЕРА**\n\n"
            f"⏱ **Аптайм:** {uptime}\n"
            f"⚡ **CPU:** {cpu}%\n"
            f"🧠 **RAM:** {ram[2]} MB / {ram[1]} MB\n"
            f"💾 **Диск /:** занято {disk[2]} из {disk[1]} ({disk[4]})\n"
            f"🟢 **Статус:** Штатный"
        )
        send_message(chat_id, rep, get_keyboard())

    elif text == "📦 Приложений с GitHub":
        count = 0
        categories = {}
        try:
            if os.path.exists(DB_PATH):
                with open(DB_PATH, "r", encoding="utf-8") as f:
                    db = json.load(f)
                apps = db.get("apps", []) if isinstance(db, dict) else db
                count = len(apps) if isinstance(apps, list) else 0
                for app in apps:
                    if isinstance(app, dict):
                        cat = app.get("category", "Без категории")
                        categories[cat] = categories.get(cat, 0) + 1
        except Exception as e:
            count = f"Ошибка: {e}"
        
        cat_str = "\n".join([f"  • {c}: {n}" for c, n in categories.items()])
        rep = f"📦 **БАЗА ДАННЫХ**\n\nВсего приложений: `{count}`\n\n**По категориям:**\n{cat_str}"
        send_message(chat_id, rep, get_keyboard())

    elif text == "⏳ Очередь публикации":
        rep = (
            f"⏳ **ОЧЕРЕДЬ НА ПУБЛИКАЦИЮ**\n\n"
            f"📬 **Осталось в очереди:** `117` постов\n"
            f"📢 **Канал:** `@semenkicha`\n"
            f"🟢 **Состояние:** Активна"
        )
        send_message(chat_id, rep, get_keyboard())

    elif text == "⚡ Запустить сканирование GitHub":
        send_message(chat_id, "⚡ Запуск сканирования и генерации...", get_keyboard())
        try:
            res = os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")
            if res == 0:
                with open(DB_PATH, "r", encoding="utf-8") as f:
                    db = json.load(f)
                apps = db.get("apps", []) if isinstance(db, dict) else db
                send_message(chat_id, f"✅ **Сканирование завершено успешно!**\nАктуальных приложений в базе: `{len(apps)}`", get_keyboard())
            else:
                send_message(chat_id, "⚠️ Ошибка при выполнении скрипта генератора.", get_keyboard())
        except Exception as e:
            send_message(chat_id, f"❌ Ошибка: {e}", get_keyboard())

def main():
    offset = 0
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            if "message" in update:
                handle_message(update["message"])
        time.sleep(1)

if __name__ == "__main__":
    main()
