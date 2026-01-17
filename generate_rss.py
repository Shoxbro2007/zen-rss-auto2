import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz

def generate_rss_feed():
    """Генерирует RSS-ленту для Яндекс Дзена"""
    
    # Настройки канала
    CHANNEL_TITLE = "Авто-Дзен тест"
    CHANNEL_LINK = "https://dzen.ru/id/66a68791ef9cc46293177763"  # ЗАМЕНИ НА СВОЙ URL!
    CHANNEL_DESCRIPTION = "Автоматически генерируемые статьи о технологиях"
    
    # Создаем корневой элемент RSS
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    # Добавляем метаданные канала
    ET.SubElement(channel, 'title').text = CHANNEL_TITLE
    ET.SubElement(channel, 'link').text = CHANNEL_LINK
    ET.SubElement(channel, 'description').text = CHANNEL_DESCRIPTION
    ET.SubElement(channel, 'language').text = 'ru'
    ET.SubElement(channel, 'generator').text = 'Zen RSS Auto Generator'
    
    # Генерируем 3 статьи
    moscow_tz = pytz.timezone('Europe/Moscow')
    
    articles = [
        {
            "title": f"Искусственный интеллект меняет мир: {datetime.now().strftime('%d.%m.%Y')}",
            "description": "Новые достижения в области ИИ открывают невероятные возможности для бизнеса и повседневной жизни. Ученые создали алгоритмы, способные предсказывать погоду с точностью до 95%.",
            "link": f"{CHANNEL_LINK}/ai-breakthrough-{datetime.now().strftime('%Y%m%d')}",
            "pub_date": (datetime.now(moscow_tz) - timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S %z')
        },
        {
            "title": f"Квантовые компьютеры: революция в вычислениях - {datetime.now().strftime('%d.%m.%Y')}",
            "description": "Квантовые процессоры начинают решать задачи, недоступные классическим компьютерам. Уже сегодня они используются для разработки новых лекарств и оптимизации логистики.",
            "link": f"{CHANNEL_LINK}/quantum-computing-{datetime.now().strftime('%Y%m%d')}",
            "pub_date": (datetime.now(moscow_tz) - timedelta(hours=2)).strftime('%a, %d %b %Y %H:%M:%S %z')
        },
        {
            "title": f"Космические технологии доступны каждому - {datetime.now().strftime('%d.%m.%Y')}",
            "description": "Миниатюрные спутники теперь могут запускать даже студенты. Космическая индустрия становится открытой для стартапов и энтузиастов.",
            "link": f"{CHANNEL_LINK}/space-tech-{datetime.now().strftime('%Y%m%d')}",
            "pub_date": (datetime.now(moscow_tz) - timedelta(hours=3)).strftime('%a, %d %b %Y %H:%M:%S %z')
        }
    ]
    
    # Добавляем статьи в RSS
    for article in articles:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = article['title']
        ET.SubElement(item, 'link').text = article['link']
        ET.SubElement(item, 'description').text = article['description']
        ET.SubElement(item, 'guid', isPermaLink='false').text = article['link']
        ET.SubElement(item, 'pubDate').text = article['pub_date']
    
    # Создаем XML-дерево и сохраняем в файл
    tree = ET.ElementTree(rss)
    tree.write('feed.xml', encoding='utf-8', xml_declaration=True)
    
    # Читаем файл и добавляем DOCTYPE (обязательно для Дзена!)
    with open('feed.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Добавляем DOCTYPE
    final_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
                   '<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n' + \
                   xml_content
    
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("✅ RSS-лента успешно создана: feed.xml")
    print(f"📄 Статьи для публикации: {len(articles)}")
    
    return 'feed.xml'

if __name__ == "__main__":
    generate_rss_feed()
