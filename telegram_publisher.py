import telebot
from telebot.types import InputMediaVideo
import requests
import os
import random
from datetime import datetime

# 🔑 НАСТРОЙКИ
BOT_TOKEN = "8493219513:AAEm-pIf7SV-fALnSN5-hSi9BrRf39ayIT0"  # ЗАМЕНИТЬ!
CHANNELS = [
    "@tech_videos",
    "@business_videos", 
    "@finance_videos"
]

def get_random_video():
    """Получает случайное видео для публикации"""
    videos = [
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
    ]
    return random.choice(videos)

def get_random_caption():
    """Генерирует случайное описание для видео"""
    captions = [
        "🔥 Искусственный интеллект меняет мир: как ИИ может сэкономить вам 3 часа в день",
        "💡 Как автоматизировать рутину: 5 инструментов, которые сократят вашу работу в 2 раза",
        "🚀 Бизнес в 2026 году: как заработать 50 000 ₽ за 1 месяц, просто автоматизировав продажи",
        "💰 Финансовая свобода: как инвестировать 10 000 ₽ и удвоить их за 2 месяца",
        "🤖 Автоматизация в действии: Zapier, который экономит 2 часа в день"
    ]
    return random.choice(captions)

def publish_to_telegram():
    """Публикует видео в Telegram каналы"""
    
    bot = telebot.TeleBot(BOT_TOKEN)
    video_url = get_random_video()
    caption = get_random_caption()
    
    success_count = 0
    
    for channel in CHANNELS:
        try:
            # Скачиваем видео локально (временно)
            response = requests.get(video_url)
            filename = f"temp_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            # Публикуем видео
            with open(filename, 'rb') as video:
                bot.send_video(
                    chat_id=channel,
                    video=video,
                    caption=caption,
                    supports_streaming=True
                )
            
            print(f"✅ Видео опубликовано в {channel}")
            success_count += 1
            
            # Удаляем временный файл
            os.remove(filename)
            
        except Exception as e:
            print(f"❌ Ошибка публикации в {channel}: {e}")
    
    print(f"🚀 Успешно опубликовано в {success_count} из {len(CHANNELS)} каналов")

if __name__ == "__main__":
    publish_to_telegram()
