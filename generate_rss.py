import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
import random
import uuid

# ВАШИ НАСТРОЙКИ
NETLIFY_BASE_URL = "https://meek-gingersnap-1bfc42.netlify.app"
CHANNEL_LINK = "https://zen.yandex.ru/id/66a68791ef9cc46293177763"

def generate_zen_article():
    """Генерирует статью для валидного RSS"""
    
    # Шаблоны статей
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
    
    template = random.choice(TEMPLATES)
    year = datetime.now().year
    num = random.randint(3, 5)
    hours = random.randint(5, 15)
    unique_id = str(uuid.uuid4())[:8]
    
    ending = "а" if num in [2, 3, 4] else "ов" if num > 4 else ""
    
    # Заполнение данных
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
    
    # Сборка текста
    title = template["title"].format(num=num, ending=ending, hours=hours, year=year) + f" [{unique_id}]"
    hook = template["hook"].format(hours=hours, year=year)
    points = "\n".join([p.format(**article_data) for p in template["points"]])
    cta = template["cta"]
    
    article_text = f"{hook}\n\n{points}\n\n{cta}"
    
    # Генерация изображения (упрощенно)
    image_url = random.choice([
        "https://picsum.photos/1200/675?random=tech1",
        "https://picsum.photos/1200/675?random=tech2",
        "https://picsum.photos/1200/675?random=ai3"
    ])
    
    # Безопасное форматирование HTML (без опасных стилей)
    safe_description = f'<img src="{image_url}" alt="Иллюстрация"/><br/>{article_text}'
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "title": title[:60] + "...",
        "content": safe_description,
        "url": f"{NETLIFY_BASE_URL}/post_{timestamp}_{unique_id}",
        "image_url": image_url,
        "pub_date": (datetime.now(pytz.timezone('Europe/Moscow')) - timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S +0300')
    }

def generate_rss_feed():
    """Генерирует валидный RSS 2.0"""
    
    CHANNEL_TITLE = "Авто-Дзен Тест"
    CHANNEL_DESCRIPTION = "Технологии будущего: автоматически генерируемый контент"
    
    # Создаем RSS 2.0 без DOCTYPE
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = CHANNEL_TITLE
    ET.SubElement(channel, 'link').text = CHANNEL_LINK
    ET.SubElement(channel, 'description').text = CHANNEL_DESCRIPTION
    ET.SubElement(channel, 'language').text = 'ru'
    ET.SubElement(channel, 'generator').text = 'Zen RSS Auto Generator v5.0'
    
    # Генерируем 3 статьи
    for i in range(3):
        article = generate_zen_article()
        
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = article['title']
        ET.SubElement(item, 'link').text = article['url']
        ET.SubElement(item, 'description').text = article['content']
        ET.SubElement(item, 'guid', attrib={'isPermaLink': 'false'}).text = article['url']
        ET.SubElement(item, 'pubDate').text = article['pub_date']
        
        # Добавляем изображение как enclosure
        enclosure = ET.SubElement(item, 'enclosure')
        enclosure.set('url', article['image_url'])
        enclosure.set('type', 'image/jpeg')
        enclosure.set('length', '123456')
    
    # Генерируем XML
    xml_content = ET.tostring(rss, encoding='unicode', method='xml')
    
    # Добавляем XML declaration вручную (без DOCTYPE)
    final_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_content
    
    # Записываем файл
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ RSS-лента создана: 3 статьи с валидным форматом")
    return 'feed.xml'

if __name__ == "__main__":
    generate_rss_feed()
