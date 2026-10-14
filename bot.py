import time
import os
import json
import requests

TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
URL = f"https://api.telegram.org/bot{TOKEN}"
REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")

def get_updates(offset=None):
    try:
        res = requests.get(f"{URL}/getUpdates", params={"timeout": 10, "offset": offset}, timeout=15)
        return res.json().get("result", [])
    except:
        return []

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(f"{URL}/sendMessage", json=data, timeout=5)
    except:
        pass

def get_keyboard():
    return {
        "keyboard": [
            [{"text": "📊 Состояние сервера"}, {"text": "📦 Приложений с GitHub"}],
            [{"text": "⏳ Очередь публикации"}, {"text": "⚡ Запустить сканирование GitHub"}]
        ],
        "resize_keyboard": True,
        "is_persistent": True
    }

def main():
    offset = 0
    print("Легковесный бот запущен...")
    while True:
        updates = get_updates(offset)
        for u in updates:
            offset = u["update_id"] + 1
            if "message" not in u:
                continue
            msg = u["message"]
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "").strip()

            if text == "/start":
                send_message(chat_id, "🛠 **Панель управления активна.**", get_keyboard())
            elif text == "📊 Состояние сервера":
                disk = os.popen("df -h / | tail -1").read().split()
                cpu = os.popen("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").read().strip()
                ram = os.popen("free -m | grep Mem").read().split()
                send_message(chat_id, f"🖥 **Сервер в норме**\n⚡ CPU: {cpu}%\n🧠 RAM: {ram[2]}MB / {ram[1]}MB\n💾 Диск /: {disk[2]} / {disk[1]}", get_keyboard())
            elif text == "📦 Приложений с GitHub":
                count = 0
                try:
                    with open(DB_PATH, "r", encoding="utf-8") as f:
                        d = json.load(f)
                    count = len(d.get("apps", [])) if isinstance(d, dict) else len(d)
                except:
                    pass
                send_message(chat_id, f"📦 Активных приложений в базе: `{count}`", get_keyboard())
            elif text == "⏳ Очередь публикации":
                try:
                    with open(DB_PATH, "r", encoding="utf-8") as f:
                        d = json.load(f)
                    q = len(d.get("apps", [])) if isinstance(d, dict) else 0
                    send_message(chat_id, f"⏳ Осталось в очереди: `{q}` постов\n📢 Канал: `@semenkicha`", get_keyboard())
                except:
                    send_message(chat_id, "⏳ Очередь пуста.", get_keyboard())
            elif text == "⚡ Запустить сканирование GitHub":
                send_message(chat_id, "⚡ Запуск сканирования...", get_keyboard())
                os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")
                send_message(chat_id, "✅ Сканирование и генерация завершены!", get_keyboard())
        
        # Увеличиваем паузу до 2 секунд, чтобы процессор полностью отдыхал
        time.sleep(2)

if __name__ == "__main__":
    main()
