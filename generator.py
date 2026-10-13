import os
import json

DB_FILE = "/root/subwtf-repo/database.json"
REPO_DIR = "/root/subwtf-repo"

def generate():
    if not os.path.exists(DB_FILE):
        return

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception:
        return

    if isinstance(raw_data, dict):
        db = raw_data.get("apps", [])
    elif isinstance(raw_data, list):
        db = raw_data
    else:
        db = []

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git App WTF — Каталог приложений</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f1115;
            --card-bg: #181c24;
            --text-main: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent: #10b981;
            --accent-glow: rgba(16, 185, 129, 0.2);
            --border: #2d3748;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ background-color: var(--bg-color); color: var(--text-main); padding-bottom: 70px; }}
        
        header {{
            position: sticky; top: 0; z-index: 100;
            background: rgba(15, 17, 21, 0.85); backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border); padding: 12px 16px;
            display: flex; align-items: center; justify-content: space-between;
        }}
        .logo {{ font-size: 20px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px; }}
        .logo span {{ color: var(--accent); }}
        
        .search-container {{ padding: 16px; max-width: 600px; margin: 0 auto; }}
        .search-box {{
            width: 100%; padding: 12px 16px 12px 42px;
            background: var(--card-bg); border: 1px solid var(--border);
            border-radius: 14px; color: #fff; font-size: 15px; outline: none;
            transition: all 0.3s ease;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: 14px center; background-size: 20px;
        }}
        .search-box:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }}

        .section-title {{ font-size: 18px; font-weight: 600; margin: 20px 16px 12px; max-width: 800px; margin-left: auto; margin-right: auto; }}
        
        .grid {{
            display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 16px; padding: 0 16px; max-width: 800px; margin: 0 auto;
        }}
        .card {{
            background: var(--card-bg); border: 1px solid var(--border);
            border-radius: 20px; padding: 14px 10px; text-align: center;
            display: flex; flex-direction: column; align-items: center;
            cursor: pointer; transition: transform 0.2s, border-color 0.2s;
            text-decoration: none; color: inherit;
        }}
        .card:hover {{ transform: translateY(-3px); border-color: var(--accent); }}
        
        .app-icon {{
            width: 64px; height: 64px; border-radius: 18px;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; font-weight: 700; color: #fff;
            margin-bottom: 10px; box-shadow: 0 6px 16px rgba(0,0,0,0.4);
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            text-transform: uppercase;
        }}
        .app-name {{ font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; margin-bottom: 4px; }}
        .app-cat {{ font-size: 11px; color: var(--text-secondary); margin-bottom: 8px; }}
        .app-size {{ font-size: 11px; background: rgba(16, 185, 129, 0.1); color: var(--accent); padding: 2px 8px; border-radius: 8px; font-weight: 600; }}

        .nav-bar {{
            position: fixed; bottom: 0; left: 0; right: 0;
            background: rgba(15, 17, 21, 0.9); backdrop-filter: blur(12px);
            border-top: 1px solid var(--border); display: flex; justify-content: space-around;
            padding: 10px 0; z-index: 100;
        }}
        .nav-item {{ color: var(--text-secondary); text-align: center; font-size: 10px; text-decoration: none; }}
        .nav-item.active {{ color: var(--accent); }}
        .nav-item svg {{ width: 22px; height: 22px; display: block; margin: 0 auto 2px; fill: currentColor; }}
    </style>
</head>
<body>

    <header>
        <div class="logo">⚡ GitApp <span>WTF</span></div>
    </header>

    <div class="search-container">
        <input type="text" class="search-box" id="search" placeholder="Поиск по каталогу..." oninput="filterApps()">
    </div>

    <div class="section-title">🔥 Доступные приложения</div>

    <div class="grid" id="app-grid">
"""

    gradients = [
        "linear-gradient(135deg, #3b82f6, #1d4ed8)",
        "linear-gradient(135deg, #10b981, #047857)",
        "linear-gradient(135deg, #f59e0b, #b45309)",
        "linear-gradient(135deg, #8b5cf6, #6d28d9)",
        "linear-gradient(135deg, #ec4899, #be185d)",
        "linear-gradient(135deg, #06b6d4, #0e7490)"
    ]

    for idx, app in enumerate(db):
        if not isinstance(app, dict):
            continue
        name = app.get("name", "App")
        category = app.get("category", "Утилиты")
        size = app.get("file_size", "15 MB")
        
        first_letter = name[0] if name else "A"
        grad = gradients[idx % len(gradients)]

        html_content += f"""
        <a class="card" href="#">
            <div class="app-icon" style="background: {grad};">{first_letter}</div>
            <div class="app-name">{name}</div>
            <div class="app-cat">{category}</div>
            <div class="app-size">{size}</div>
        </a>
        """

    html_content += f"""
    </div>

    <div class="nav-bar">
        <a href="#" class="nav-item active">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            Главная
        </a>
        <a href="#" class="nav-item">
            <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
            Поиск
        </a>
    </div>

    <script>
        function filterApps() {{
            let query = document.getElementById('search').value.toLowerCase();
            let cards = document.querySelectorAll('.card');
            cards.forEach(card => {{
                let name = card.querySelector('.app-name').innerText.toLowerCase();
                card.style.display = name.includes(query) ? 'flex' : 'none';
            }});
        }}
    </script>
</body>
</html>
"""

    output_path = os.path.join(REPO_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate()
