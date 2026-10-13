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
    print(f"[DAEMON] {msg}")
    with open(os.path.join(REPO_PATH, "daemon.log"), "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def job():
    log("Запуск цикла сканирования GitHub и обновления каталога...")
    
    # 1. Запуск генератора / парсера (предполагаем, что generator.py или отдельный скрипт парсинга обновляет database.json)
    # Если у вас есть отдельный скрипт парсинга (например parser.py), вызывайте его. Сейчас вызываем генератор и git sync.
    res_gen = os.system(f"python3 {os.path.join(REPO_PATH, 'generator.py')}")
    if res_gen != 0:
        log("Ошибка при выполнении генератора.")
        return

    # 2. Автоматический Git Commit & Push на GitHub
    git_cmd = f"cd {REPO_PATH} && git add . && git commit -m 'Auto-daemon: update database and site' && git push origin main"
    res_git = os.system(git_cmd)
    if res_git == 0:
        log("Сайт успешно пересобран и отправлен на GitHub.")
    else:
        log("Ошибка отправки изменений в Git (возможно, нет новых коммитов).")

    # 3. Автоматическая публикация свежего приложения в Telegram-канал
    try:
        if os.path.exists(DB_PATH):
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            apps = data.get("apps", []) if isinstance(data, dict) else data
            
            if apps and isinstance(apps, list):
                # Берем первое или самое свежее приложение
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
                    f"👉 Скачать и найти другие приложения можно на нашем сайте!"
                )
                
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
                log(f"Пост о приложении '{name}' успешно отправлен в канал {CHANNEL_ID}.")
    except Exception as e:
        log(f"Ошибка автопубликации в канал: {e}")

def main():
    log("Демон автопилота запущен и готов рвать GitHub.")
    while True:
        try:
            job()
        except Exception as e:
            log(f"Ошибка в цикле демона: {e}")
        
        # Интервал проверки (например, каждые 2 часа = 7200 секунд)
        time.sleep(7200)

if __name__ == "__main__":
    main()
