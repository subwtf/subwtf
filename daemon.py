import time
import os
import json
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
    # 1. Генерация уникального сайта
    res_gen = os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")
    if res_gen != 0:
        return

    # 2. Проверяем базу и публикуем только новые (не архивные) приложения
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if isinstance(data, dict):
                apps = data.get("apps", [])
                archive = data.get("archive", [])
            else:
                apps = data
                archive = []

            if apps and isinstance(apps, list):
                # Берем самое первое приложение из списка
                app = apps.pop(0)
                name = app.get('name', 'App')
                
                # Проверяем, нет ли его уже в архиве
                archive_names = [a.get('name') for a in archive if isinstance(a, dict)]
                if name not in archive_names:
                    cat = app.get('category', 'Утилиты')
                    rating = app.get('rating', '-')
                    size = app.get('file_size', 'N/A')
                    desc = app.get('desc', 'Описание отсутствует.')[:200]
                    
                    text = (
                        f"🔥 **Новый релиз:** *{name}*\n"
                        f"📂 Категория: {cat}\n"
                        f"⭐ Рейтинг: {rating} | 📦 Размер: {size}\n\n"
                        f"📝 {desc}...\n\n"
                        f"👉 Каталог приложений: https://subwtf.github.io/subwtf/"
                    )
                    
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    res = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
                    
                    if res.status_code == 200:
                        log(f"Опубликовано и уведено в архив: '{name}'")
                        archive.append(app)
                        
                        # Сохраняем обновленные списки обратно в JSON
                        data["apps"] = apps
                        data["archive"] = archive
                        with open(DB_PATH, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            log(f"Ошибка в цикле публикации: {e}")

    # 3. Синхронизация с GitHub
    git_cmd = f"cd {REPO_PATH} && git add . && git commit -m 'Daemon: archive sync and update' && git push origin main"
    os.system(git_cmd)

def main():
    log("Демон защиты от повторов запущен.")
    while True:
        try:
            job()
        except Exception as e:
            log(f"Ошибка: {e}")
        time.sleep(300) # Интервал между проверками

if __name__ == "__main__":
    main()
