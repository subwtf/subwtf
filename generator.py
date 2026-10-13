import os
import datetime

TOPICS = [
    ("Настройка прокси и обхода блокировок через Xray", "Полное руководство по развертыванию протоколов нового поколения для безопасной передачи данных.", "xray-guide.html"),
    ("Оптимизация производительности Ubuntu VPS 1GB RAM", "Тонкая настройка ядра Linux, отключение лишних служб и управление SWAP-памятью для слабой виртуальной машины.", "ubuntu-optimization.html"),
    ("Автоматизация бэкапов в Docker: практические примеры", "Надежные скрипты для ежедневного сохранения баз данных и конфигураций без потери производительности.", "docker-backups.html"),
]

def generate_index(articles):
    cards_html = ""
    for title, desc, filename in articles:
        cards_html += f"""
                <article class="group rounded-2xl bg-slate-50 border border-slate-200/80 p-6 hover:bg-white hover:border-emerald-500/50 hover:shadow-xl hover:shadow-emerald-500/5 transition-all flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4">
                            <span class="px-3 py-1 rounded-lg bg-emerald-100/80 text-emerald-800 text-xs font-semibold">Инфраструктура</span>
                            <span class="text-xs text-slate-400">2026</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 group-hover:text-emerald-600 transition-colors mb-3">
                            {title}
                        </h3>
                        <p class="text-slate-600 text-sm leading-relaxed mb-6">
                            {desc}
                        </p>
                    </div>
                    <a href="{filename}" class="inline-flex items-center gap-2 text-sm font-bold text-slate-900 group-hover:text-emerald-600 transition-colors">
                        <span>Читать статью</span>
                        <i class="fa-solid fa-arrow-right text-xs transition-transform group-hover:translate-x-1"></i>
                    </a>
                </article>
"""

    return f"""<!DOCTYPE html>
<html lang="ru" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexTech Lab — Инженерный блогинг, инфраструктура и сетевые технологии нового поколения</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased">
    <header class="sticky top-0 z-50 backdrop-blur-md bg-white/80 border-b border-slate-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <a href="index.html" class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-white shadow-lg">
                    <i class="fa-solid fa-bolt text-lg"></i>
                </div>
                <span class="text-xl font-extrabold tracking-tight text-slate-900">NexTech<span class="text-emerald-600">.Lab</span></span>
            </a>
        </div>
    </header>
    <section class="relative overflow-hidden pt-20 pb-16">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <h1 class="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight mb-6">
                Автономный хаб инженерных <span class="text-emerald-600">решений</span>
            </h1>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto">Свежие практические материалы и руководства по настройке серверов и сетей.</p>
        </div>
    </section>
    <section class="py-12 bg-white border-t border-slate-100">
        <div class="max-w-7xl mx-auto px-4">
            <h2 class="text-2xl font-bold text-slate-900 mb-8">Все публикации</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                {cards_html}
            </div>
        </div>
    </section>
</body>
</html>
"""

def generate_article(title, desc, filename):
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — NexTech Lab</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-50 text-slate-800 font-sans">
    <header class="bg-white border-b border-slate-100 py-4 px-8">
        <a href="index.html" class="text-emerald-600 font-bold">&larr; На главную</a>
    </header>
    <main class="max-w-3xl mx-auto px-4 py-12">
        <h1 class="text-3xl font-extrabold text-slate-900 mb-4">{title}</h1>
        <p class="text-lg text-slate-600 mb-8">{desc}</p>
        <div class="bg-white p-8 rounded-2xl border border-slate-200 space-y-4">
            <p>Детальный разбор архитектуры и пошаговая реализация поставленной задачи на практике.</p>
            <div class="bg-slate-900 text-slate-200 p-4 rounded-xl font-mono text-sm">
                # Пример конфигурации<br>echo "Running automation task..."
            </div>
        </div>
    </main>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

articles = []
for title, desc, filename in TOPICS:
    generate_article(title, desc, filename)
    articles.append((title, desc, filename))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(generate_index(articles))

print("Все статьи и главная страница сгенерированы!")
