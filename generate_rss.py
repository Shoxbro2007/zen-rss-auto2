import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
import random
import uuid
import hashlib

def generate_zen_article():
    """Генерирует статью в формате, совместимом с Дзеном"""
    
    topics = ["Технологии", "Бизнес", "Финансы", "Продуктивность", "Криптовалюта"]
    keywords = ["бесплатно", "секрет", "за 5 минут", "работает", "доход", "идея", "без вложений"]
    
    title = f"{random.choice(keywords).capitalize()} {random.choice(topics)}: {random.randint(3, 5)} способов заработать в {datetime.now().year}"
    
    hook = f"Вы не поверите, но я заработал {random.randint(5000, 50000)} ₽ за {random.randint(1, 3)} месяца, просто автоматизировав {random.choice(['продажи', 'маркетинг', 'инвестиции'])}. Вот как это сделать."
    
    main_points = [
        f"❌ Проблема: {random.choice(['много времени', 'низкая эффективность', 'мало дохода'])}",
        f"✅ Решение: {random.choice(['автоматизация', 'инвестиции', 'система'])}",
        f"🎯 Результат: {random.choice(['свободное время', 'стабильный доход', 'рост'])}"
    ]
    
    conclusion = f"Попробуйте сами - результат не заставит себя ждать! {random.choice(['Сохраните пост - пригодится!', 'Пишите в комментариях, что у вас получилось!'])}"
    
    image_url = random.choice([
        "https://picsum.photos/1200/675?random=tech1",
        "https://picsum.photos/1200/675?random=business2",
        "https://picsum.photos/1200/675?random=finance3",
        "https://picsum.photos/1200/675?random=productivity4",
        "https://picsum.photos/1200/675?random=crypto5"
    ])
    
    content_encoded = f"""<p>{hook}</p>
<figure>
<img src="{image_url}" alt="Иллюстрация"/>
<figcaption>Первый андроид-фермер смотрит на свои угодья</figcaption>
</figure>
<p>{chr(10).join(main_points)}</p>
<p>{conclusion}</p>
<p>#{' '.join(random.sample(keywords, 2))} #{random.choice(topics)}</p>"""
    
    unique_id = str(uuid.uuid4())[:8]
    guid = hashlib.sha256(f"{title}{unique_id}".encode()).hexdigest()[:40]
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    pub_date = (datetime.now(moscow_tz) - timedelta(minutes=random.randint(1, 60))).strftime('%a, %d %b %Y %H:%M:%S +0300')
    
    return {
        "title": title,
        "content_encoded": content_encoded,
        "url": f"https://shoxbro2007.github.io/zen-rss-auto2/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}",
        "image_url": image_url,
        "guid": guid,
        "pub_date": pub_date,
        "description": hook[:150]
    }

def generate_zen_rss_feed():
    """Генерирует RSS-ленту как HTML файл"""
    
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    rss.set('xmlns:media', 'http://search.yahoo.com/mrss/')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    rss.set('xmlns:georss', 'http://www.georss.org/georss')
    
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = "Авто-Дзен Тест"
    ET.SubElement(channel, 'link').text = "https://zen.yandex.ru/id/66a68791ef9cc46293177763"
    ET.SubElement(channel, 'description').text = "Автоматически генерируемый контент для Яндекс Дзена"
    ET.SubElement(channel, 'language').text = 'ru'
    ET.SubElement(channel, 'generator').text = 'Zen RSS Auto Generator v7.0'
    
    # Генерируем 3 статьи
    for i in range(3):
        article = generate_zen_article()
        
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = article['title']
        ET.SubElement(item, 'link').text = article['url']
        ET.SubElement(item, 'pdalink').text = article['url']
        ET.SubElement(item, 'guid', isPermaLink='false').text = article['guid']
        ET.SubElement(item, 'pubDate').text = article['pub_date']
        ET.SubElement(item, 'description').text = article['description']
        
        enclosure = ET.SubElement(item, 'enclosure')
        enclosure.set('url', article['image_url'])
        enclosure.set('type', 'image/jpeg')
        enclosure.set('length', '123456')
        
        content = ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded')
        content.text = article['content_encoded']
        
        ET.SubElement(item, 'category').text = 'native-draft'
        ET.SubElement(item, 'category').text = 'format-article'
        ET.SubElement(item, 'category').text = 'index'
        ET.SubElement(item, 'category').text = 'comment-all'
    
    # Генерируем как HTML (с DOCTYPE)
    xml_content = ET.tostring(rss, encoding='unicode', method='xml')
    final_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
                   '<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n' + \
                   xml_content
    
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("✅ RSS-лента создана как feed.xml")

if __name__ == "__main__":
    generate_zen_rss_feed()
