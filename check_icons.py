import json

with open("/root/subwtf-repo/database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for i in range(min(5, len(db))):
    item = db[i]
    if isinstance(item, dict):
        print(f"App: {item.get('name')} | icon_url: {item.get('icon_url')} | icon: {item.get('icon')}")
