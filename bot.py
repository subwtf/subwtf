import logging
import subprocess
import os
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

TOKEN = "8794166379:AAGsYMxjmfSRvfR7dDoF0qfv-yFRaM-df-g"
REPO_PATH = "/root/subwtf-repo"
DB_PATH = os.path.join(REPO_PATH, "database.json")
LOG_PATH = os.path.join(REPO_PATH, "bot.log")

# ID чата или канала, куда слать авто-посты (сюда будет писать бот каждые 10 минут)
# Если хочешь, чтобы он писал туда же, откуда вызывают, или в конкретный чат/группу/ID:
# Замени на свой ID чата или используй ID администратора/чата по умолчанию
TARGET_CHAT_ID = None  # Если None, будет пытаться брать из последнего сообщения или можно прописать ID вручную

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главная клавиатура (всегда внизу)
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Состояние Машины"), KeyboardButton(text="⚙️ Генерация и Сайт")],
            [KeyboardButton(text="🚀 Git & Деплой"), KeyboardButton(text="🛠 Логи и Управление")]
        ],
        resize_keyboard=True,
        is_persistent=True
    )

# --- ФОНОВАЯ ЗАДАЧА: АВТОПОСТИНГ КАЖДЫЕ 10 МИНУТ ---
async def background_poster():
    """Каждые 10 минут берет по 4-5 приложений из базы и шлет пулом с иконками"""
    await asyncio.sleep(5)  мощный старт после запуска
    while True:
        try:
            if os.path.exists(DB_PATH):
                with open(DB_PATH, "r", encoding="utf-8") as f:
                    db = json.load(f)
                
                if isinstance(db, list) and len(db) > 0:
                    # Берем первые 5 элементов (или можно сделать ротацию)
                    batch = db[:5]
                    
                    post_text = "🔥 **Свежая подборка приложений и релизов:**\n\n"
                    media_group = []
                    
                    for i, app in enumerate(batch):
                        name = app.get("name", "Приложение")
                        category = app.get("category", "Разное")
                        rating = app.get("rating", "-")
                        file_size = app.get("file_size", "Не указан")
                        date = app.get("date", "Не указана")
                        desc = app.get("desc", "Описание отсутствует.")
                        icon = app.get("icon_url", "")
                        
                        post_text += (
                            f"📌 **{name}** ({category})\n"
                            f"⭐ Рейтинг: {rating} | 📦 Размер: {file_size} | 📅 Дата: {date}\n"
                            f"📝 {desc[:150]}...\n\n"
                        )
                    
                    # Если задан TARGET_CHAT_ID, шлем туда
                    # (Для теста можно сохранить ID последнего чата, куда тыкнули бота)
                    global LAST_ACTIVE_CHAT_ID
                    if 'LAST_ACTIVE_CHAT_ID' in globals() and LAST_ACTIVE_CHAT_ID:
                        await bot.send_message(LAST_ACTIVE_CHAT_ID, post_text, parse_mode="Markdown")
                        
            await asyncio.sleep(600)  # Ждем 10 минут (600 секунд)
        except Exception as e:
            logging.error(f"Ошибка в фоновом автопостинге: {e}")
            await asyncio.sleep(60)

# Глобальная переменная для запоминания чата
LAST_ACTIVE_CHAT_ID = None

# --- 1. СТАТУС И ЗДОРОВЬЕ СЕРВЕРА ---
@dp.message_handler(lambda message: message.text == "📊 Состояние Машины")
async def cmd_status(message: types.Message):
    global LAST_ACTIVE_CHAT_ID
    LAST_ACTIVE_CHAT_ID = message.chat.id
    
    disk = os.popen("df -h / | tail -1").read().split()
    cpu = os.popen("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").read().strip()
    ram = os.popen("free -m | grep Mem").read().split()
    
    db_status = "🟢 В норме (Валидный JSON)"
    db_details = ""
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        db_details = f"📦 Записей в базе: {len(data) if isinstance(data, list) else 'Объект'}"
    except Exception as e:
        db_status = f"🔴 ОШИБКА В JSON!"
        db_details = f"⚠️ {str(e)}"

    text = (
        f"🖥 **ТЕЛЕМЕТРИЯ СЕРВЕРА & МАШИНЫ**\n\n"
        f"⚡ **CPU загрузка:** {cpu}%\n"
        f"🧠 **RAM:** {ram[2]}MB / {ram[1]}MB (Свободно: {ram[3]}MB)\n"
        f"💾 **Диск /:** занято {disk[2]} из {disk[1]} ({disk[4]})\n\n"
        f"🗄 **База данных (`database.json`):**\n"
        f"Статус: {db_status}\n"
        f"{db_details}"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 Проверить JSON", callback_data="check_json"),
        InlineKeyboardButton("🔄 Обновить статус", callback_data="refresh_status")
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=markup)

# --- 2. ГЕНЕРАЦИЯ И САЙТ ---
@dp.message_handler(lambda message: message.text == "⚙️ Генерация и Сайт")
async def cmd_generation_menu(message: types.Message):
    global LAST_ACTIVE_CHAT_ID
    LAST_ACTIVE_CHAT_ID = message.chat.id
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🚀 Пересобрать сайт (generator.py)", callback_data="run_generator"),
        InlineKeyboardButton("🔍 Валидация базы данных", callback_data="check_json"),
        InlineKeyboardButton("🌐 Проверить статус Git / Репо", callback_data="git_status")
    )
    await message.answer(
        "⚙️ **Панель управления контентом и генератором:**\nВыберите нужное действие:",
        parse_mode="Markdown",
        reply_markup=markup
    )

# --- 3. GIT И ДЕПЛОЙ ---
@dp.message_handler(lambda message: message.text == "🚀 Git & Деплой")
async def cmd_git_menu(message: types.Message):
    global LAST_ACTIVE_CHAT_ID
    LAST_ACTIVE_CHAT_ID = message.chat.id
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📦 Git Status", callback_data="git_status"),
        InlineKeyboardButton("📤 Push на GitHub", callback_data="git_push")
    )
    
    status_out = os.popen(f"cd {REPO_PATH} && git status -s").read().strip()
    status_text = "✨ Репозиторий чист, изменений нет." if not status_out else f"📝 **Измененные файлы:**\n```\n{status_out}\n```"

    await message.answer(
        f"🚀 **Центр развертывания (Git):**\n\n{status_text}",
        parse_mode="Markdown",
        reply_markup=markup
    )

# --- 4. ИНСТРУМЕНТЫ И ЛОГИ ---
@dp.message_handler(lambda message: message.text == "🛠 Логи и Управление")
async def cmd_tools_menu(message: types.Message):
    global LAST_ACTIVE_CHAT_ID
    LAST_ACTIVE_CHAT_ID = message.chat.id
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📄 Хвост логов (bot.log)", callback_data="view_logs"),
        InlineKeyboardButton("🔄 Перезапустить бота", callback_data="restart_bot")
    )
    await message.answer(
        "🛠 **Системные инструменты и отладка:**",
        parse_mode="Markdown",
        reply_markup=markup
    )

# --- ОБРАБОТЧИК КНОПОК (ИНЛАЙН ЛОГИКА) ---
@dp.callback_query_handler(lambda c: True)
async def process_callbacks(callback_query: types.CallbackQuery):
    code = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    
    if code == "check_json":
        try:
            res = subprocess.run(["python3", "-m", "json.tool", DB_PATH], capture_output=True, text=True)
            if res.returncode == 0:
                await bot.send_message(callback_query.from_user.id, "✅ **JSON безупречен!** Ошибок синтаксиса не обнаружено.", parse_mode="Markdown")
            else:
                await bot.send_message(callback_query.from_user.id, f"❌ **Найдены ошибки в базе:**\n```\n{res.stderr}\n```", parse_mode="Markdown")
        except Exception as e:
            await bot.send_message(callback_query.from_user.id, f"❌ Ошибка проверки: {e}")

    elif code == "run_generator":
        await bot.send_message(callback_query.from_user.id, "🚀 Запускаю генератор сайта...")
        try:
            res = subprocess.run(["python3", os.path.join(REPO_PATH, "generator.py")], capture_output=True, text=True, timeout=45)
            if res.returncode == 0:
                await bot.send_message(callback_query.from_user.id, "✅ **Генерация успешно завершена!** Сайт пересобран.", parse_mode="Markdown")
            else:
                await bot.send_message(callback_query.from_user.id, f"⚠️ **Ошибка генератора:**\n```\n{res.stderr[-800:]}\n```", parse_mode="Markdown")
        except Exception as e:
            await bot.send_message(callback_query.from_user.id, f"❌ Таймаут или сбой выполнения: {e}")

    elif code == "git_status":
        out = os.popen(f"cd {REPO_PATH} && git status").read()
        await bot.send_message(callback_query.from_user.id, f"📦 **Git Status:**\n```\n{out}\n```", parse_mode="Markdown")

    elif code == "git_push":
        await bot.send_message(callback_query.from_user.id, "📤 Выполняю коммит и пуш на GitHub...")
        cmd = f"cd {REPO_PATH} && git add . && git commit -m 'Auto-update via bot panel' && git push origin main"
        res = os.popen(cmd).read()
        await bot.send_message(callback_query.from_user.id, f"✅ **Результат деплоя:**\n```\n{res}\n```", parse_mode="Markdown")

    elif code == "view_logs":
        if os.path.exists(LOG_PATH):
            logs = os.popen(f"tail -n 20 {LOG_PATH}").read()
            await bot.send_message(callback_query.from_user.id, f"📄 **Последние логи бота:**\n```\n{logs}\n```", parse_mode="Markdown")
        else:
            await bot.send_message(callback_query.from_user.id, "📄 Файл логов пуст или отсутствует.")

    elif code == "refresh_status":
        await cmd_status(callback_query.message)

    elif code == "restart_bot":
        await bot.send_message(callback_query.from_user.id, "🔄 Перезапускаю систему...")
        os._exit(0)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global LAST_ACTIVE_CHAT_ID
    LAST_ACTIVE_CHAT_ID = message.chat.id
    
    await message.answer(
        "🔥 **Панель управления 'Промышленный Комбайн' активирована.**\nАвтопостинг каждые 10 минут активен. Выберите нужный модуль внизу 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    from aiogram import executor
    print("Промышленный комбайн с автопостингом запущен...")
    # Запускаем фоновую задачу планировщика вместе с ботом
    loop = asyncio.get_event_loop()
    loop.create_task(background_poster())
    executor.start_polling(dp, skip_updates=True)
