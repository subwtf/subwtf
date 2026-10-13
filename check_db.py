import json

with open("/root/subwtf-repo/database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

print("Тип корневого объекта:", type(db))
if isinstance(db, dict):
    print("Ключи словаря:", list(db.keys()))
    # Посмотрим первый ключ, если это контейнер
    first_key = list(db.keys())[0] if db else None
    if first_key and isinstance(db[first_key], list):
        print(f"Элементов в ключе '{first_key}':", len(db[first_key]))
        print("Пример объекта:", db[first_key][0] if db[first_key] else "Пусто")
elif isinstance(db, list):
    print("Всего элементов в списке:", len(db))
    print("Пример объекта:", db[0] if db else "Пусто")
