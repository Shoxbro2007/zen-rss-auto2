import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
import random
import uuid
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import base64
from io import BytesIO

# ВАШИ НАСТРОЙКИ (ЗАМЕНИТЕ НА СВОИ)
NETLIFY_BASE_URL = "https://meek-gingersnap-1bfc42.netlify.app"  # Ваш Netlify URL
CHANNEL_LINK = "https://dzen.ru/id/66a68791ef9cc46293177763"  # Замените на ваш ID канала Дзен

def generate_zen_article():
    """Генерирует статью с уникальным ID и правильным форматом"""
    
    # 🧠 1. ВСТРОЕННАЯ БАЗА ШАБЛОНОВ
    TEMPLATES = [
        {
            "title": "🔥 {num} Секрет{ending}, Которые Сэкономят Вам {hours} Часов В Неделю!",
            "hook": "Вы тратите {hours} часов в неделю на то, что можно автоматизировать за 7 минут?",
            "points": [
                "✅ 1. {tool1} - {benefit1}",
                "✅ 2. {tool2} - {benefit2}",
                "✅ 3. {tool3} - {benefit3}"
            ],
            "cta": "👉 Сохраните этот пост - завтра эти инструменты могут стать платными!"
        },
        {
            "title": "💡 {num} Прост{ending} Способ{ending} Заработать В {year}",
            "hook": "Знаете ли вы, что 80% людей пропускают этот простой метод заработка?",
            "points": [
                "✅ 1. {method1} - {result1}",
                "✅ 2. {method2} - {result2}",
                "✅ 3. {method3} - {result3}"
            ],
            "cta": "🔥 Подписывайтесь - завтра расскажу о скрытых возможностях!"
        }
    ]
    
    # 🎲 2. РАНДОМИЗАЦИЯ
    template = random.choice(TEMPLATES)
    year = datetime.now().year
    num = random.randint(3, 5)
    hours = random.randint(5, 15)
    unique_id = str(uuid.uuid4())[:8]  # УНИКАЛЬНЫЙ ID ДЛЯ СТАТЬИ
    
    # Склонение окончаний
    ending = "а" if num in [2, 3, 4] else "ов" if num > 4 else ""
    
    # 🛠️ 3. ЗАПОЛНЕНИЕ ШАБЛОНА
    if "Секрет" in template["title"]:
        article_data = {
            "tool1": random.choice(["Автоматизация в Telegram", "AI-ассистенты", "Zapier"]), 
            "benefit1": random.choice(["сэкономит 3 часа", "удвоит скорость работы", "избавит от рутины"]),
            "tool2": random.choice(["Canva Magic", "Google Sheets + ИИ", "CapCut"]),
            "benefit2": random.choice(["создаст контент за вас", "автоматизирует отчеты", "ускорит монтаж"]),
            "tool3": random.choice(["Яндекс Дзен RSS", "VK API", "GitHub Actions"]),
            "benefit3": random.choice(["опубликует посты сам", "соберет аудиторию", "заменит менеджера"])
        }
    else:
        article_data = {
            "method1": random.choice(["Партнерские программы", "Продажа шаблонов", "Контент для бизнеса"]),
            "result1": random.choice(["+50 000 ₽/месяц", "пассивный доход", "клиенты из соцсетей"]),
            "method2": random.choice(["Автоматизация в ВК", "Telegram-боты", "Реклама в Дзене"]),
            "result2": random.choice(["100+ заявок в день", "автоматические продажи", "рост в 2x"]),
            "method3": random.choice(["AI-генерация контента", "RSS-импорт", "Видео из текста"]),
            "result3": random.choice(["контент на месяц за 1 час", "10 каналов за цену одного", "вирусные ролики"])
        }
    
    # ✨ 4. СБОРКА ТЕКСТА С УНИКАЛЬНЫМ ID
    title = template["title"].format(num=num, ending=ending, hours=hours, year=year) + f" [{unique_id}]"
    hook = template["hook"].format(hours=hours, year=year)
    points = "\n".join([p.format(**article_data) for p in template["points"]])
    cta = template["cta"]
    
    article_text = f"{hook}\n\n{points}\n\n{cta}"
    
    # 🖼️ 5. ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЯ
    try:
        # Бесплатные стоковые фото
        stock_url = random.choice([
            "https://picsum.photos/1200/675?grayscale",
            "https://picsum.photos/1200/675?blur=2",
            "https://picsum.photos/1200/675?nature",
            "https://picsum.photos/1200/675?technology"
        ])
        
        # Добавляем текст заголовка поверх изображения
        response = requests.get(stock_url, timeout=10)
        img = Image.open(BytesIO(response.content))
        
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arialbd.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        # Разбиваем заголовок на строки
        wrapped_title = textwrap.fill(title[:30], width=25)
        
        # Позиция текста
        text_bbox = draw.textbbox((0, 0), wrapped_title, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        x = (img.width - text_width) / 2
        y = img.height * 0.1
        
        # Добавляем полупрозрачный фон под текст
        draw.rectangle([
            (x - 20, y - 10),
            (x + text_width + 20, y + text_bbox[3] - text_bbox[1] + 10)
        ], fill=(0, 0, 0, 180))
        
        # Белый текст с обводкой
        draw.text((x, y), wrapped_title, font=font, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        
        # Сохраняем в памяти
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85)
        img_byte_arr.seek(0)
        
        # Загружаем на ImgBB
        api_url = "https://api.imgbb.com/1/upload"
        params = {
            "key": "20a4b69a0c8f1ce2c56a8e6c0a1b5e5d",
            "image": base64.b64encode(img_byte_arr.read()).decode('utf-8')
        }
        
        response = requests.post(api_url, data=params, timeout=15)
        if response.status_code == 200:
            image_url = response.json()['data']['url']
        else:
            image_url = stock_url
            
    except Exception as e:
        print(f"⚠️ Ошибка генерации изображения: {e}")
        image_url = random.choice([
            "https://picsum.photos/1200/675?random=tech1",
            "https://picsum.photos/1200/675?random=tech2"
        ])
    
    # 🔥 6. ФИНАЛЬНЫЙ ФОРМАТ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "title": title[:60] + "...",
        "content": f'<img src="{image_url}" alt="Иллюстрация" style="max-width:100%;margin:20px 0"/><br/>' + article_text,
        "url": f"{NETLIFY_BASE_URL}/post_{timestamp}_{unique_id}",
        "image_url": image_url,
        "pub_date": (datetime.now(pytz.timezone('Europe/Moscow')) - timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S +0300')
    }

def generate_rss_feed():
    """Генерирует RSS-ленту без ошибок XML"""
    
    CHANNEL_TITLE = "Авто-Дзен Тест"
    CHANNEL_DESCRIPTION = "Технологии будущего: автоматически генерируемый контент"
    
    # Создаем XML-структуру
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = CHANNEL_TITLE
    ET.SubElement(channel, 'link').text = CHANNEL_LINK
    ET.SubElement(channel, 'description').text = CHANNEL_DESCRIPTION
    ET.SubElement(channel, 'language').text = 'ru'
    ET.SubElement(channel, 'generator').text = 'Zen RSS Auto Generator v4.0'
    
    # Генерируем 3 статьи
    articles = []
    
    for i in range(3):
        article = generate_zen_article()
        articles.append(article)
        
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = article['title']
        ET.SubElement(item, 'link').text = article['url']
        ET.SubElement(item, 'description').text = article['content']
        ET.SubElement(item, 'guid', isPermaLink='false').text = article['url']
        ET.SubElement(item, 'pubDate').text = article['pub_date']  # ПРАВИЛЬНЫЙ ФОРМАТ ДАТЫ
        
        # Добавляем изображение как enclosure
        enclosure = ET.SubElement(item, 'enclosure')
        enclosure.set('url', article['image_url'])
        enclosure.set('type', 'image/jpeg')
        enclosure.set('length', '123456')
    
    # ГЕНЕРИРУЕМ XML БЕЗ ОШИБОК
    xml_content = ET.tostring(rss, encoding='utf-8', method='xml').decode('utf-8')
    
    # ФОРМИРУЕМ ФИНАЛЬНЫЙ КОНТЕНТ С ТОЧНЫМ ФОРМАТОМ
    final_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
                   '<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n' + \
                   xml_content
    
    # ЗАПИСЫВАЕМ БЕЗ ЛИШНИХ ПРОБЕЛОВ
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(final_content.strip())  # Удаляем лишние пробелы
    
    print(f"✅ RSS-лента создана: {len(articles)} статей с правильным форматом")
    return 'feed.xml'

if __name__ == "__main__":
    generate_rss_feed()
