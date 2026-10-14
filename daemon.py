import time
import os
import json
import requests

REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")
TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
CHANNEL_ID = "@semenkicha"

def log(msg):
    with open(os.path.join(REPO_PATH, "daemon.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def job():
    os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            apps = data.get("apps", []) if isinstance(data, dict) else data
            archive = data.get("archive", []) if isinstance(data, dict) else []

            if apps and isinstance(apps, list):
                app = apps.pop(0)
                name = app.get('name', 'App')
                cat = app.get('category', 'Утилиты')
                size = app.get('file_size', 'N/A')
                desc = app.get('desc', 'Описание отсутствует.')[:200]
                
                text = (
                    f"🔥 **Новый релиз:** *{name}*\n"
                    f"📂 Категория: {cat} | 📦 Размер: {size}\n\n"
                    f"📝 {desc}...\n\n"
                    f"👉 Каталог: https://subwtf.github.io/subwtf/"
                )
                
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
                if res.status_code == 200:
                    archive.append(app)
                    data["apps"] = apps
                    data["archive"] = archive
                    with open(DB_PATH, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    log(f"Опубликовано: {name}")
        except Exception as e:
            log(f"Ошибка: {e}")

    os.system(f"cd {REPO_PATH} && git add . && git commit -m 'Auto daemon sync' && git push origin main")

def main():
    while True:
        try:
            job()
        except Exception as e:
            log(f"Error: {e}")
        # Проверка и публикация каждые 15 минут (900 секунд), чтобы процессор отдыхал
        time.sleep(900)

if __name__ == "__main__":
    main()
