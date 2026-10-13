import time
import os
import json
import subprocess
import requests

REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")
TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
CHANNEL_ID = "@semenkicha"

def log(msg):
    print(f"[DAEMON 24/7] {msg}")
    with open(os.path.join(REPO_PATH, "daemon.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def job():
    log("Штурм GitHub: запуск поиска и обновления...")
    
    # 1. Запуск генератора / парсера
    res_gen = os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")
    if res_gen != 0:
        log("Ошибка генератора, повторим попытку в следующем цикле.")
        return

    # 2. Автоматический Git Commit & Push
    git_cmd = f"cd {REPO_PATH} && git add . && git commit -m 'Daemon 24/7: auto-sync database and site' && git push origin main"
    os.system(git_cmd)

    # 3. Публикация в канал
    try:
        if os.path.exists(DB_PATH):
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            apps = data.get("apps", []) if isinstance(data, dict) else data
            
            if apps and isinstance(apps, list):
                app = apps[0]
                name = app.get('name', 'App')
                cat = app.get('category', 'Утилиты')
                rating = app.get('rating', '-')
                size = app.get('file_size', 'N/A')
                desc = app.get('desc', 'Описание отсутствует.')[:250]
                
                text = (
                    f"🔥 **Новый релиз в каталоге:** *{name}*\n"
                    f"📂 Категория: {cat}\n"
                    f"⭐ Рейтинг: {rating} | 📦 Размер: {size}\n\n"
                    f"📝 {desc}...\n\n"
                    f"👉 Скачать: https://subwtf.github.io/subwtf/"
                )
                
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
                log(f"Пост о приложении '{name}' отправлен в канал.")
    except Exception as e:
        log(f"Ошибка публикации: {e}")

def main():
    log("Демон 24/7 запущен на полную мощность. Погнали!")
    while True:
        try:
            job()
        except Exception as e:
            log(f"Ошибка в цикле: {e}")
        
        # Небольшая пауза в 60 секунд между итерациями, чтобы не упереться в лимиты API GitHub
        time.sleep(60)

if __name__ == "__main__":
    main()
