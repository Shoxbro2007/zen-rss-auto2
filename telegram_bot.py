import telebot
import requests
import random

# НАСТРОЙКИ
BOT_TOKEN = "8493219513:AAEm-pIf7SV-fALnSN5-hSi9BrRf39ayIT0"  # ЗАМЕНИТЬ!
CHANNELS = [-1003565841702, -1003869947131, -1003761672782]  # ЗАМЕНИТЬ НА ВАШИ ID!

# ВИДЕО ДЛЯ ПУБЛИКАЦИИ
VIDEOS = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
]

# ОПИСАНИЯ
CAPTIONS = [
    "🔥 Искусственный интеллект меняет мир: как ИИ может сэкономить вам 3 часа в день",
    "💡 Как автоматизировать рутину: 5 инструментов, которые сократят вашу работу в 2 раза",
    "🚀 Бизнес в 2026 году: как заработать 50 000 ₽ за 1 месяц, просто автоматизировав продажи",
    "💰 Финансовая свобода: как инвестировать 10 000 ₽ и удвоить их за 2 месяца",
    "🤖 Автоматизация в действии: Zapier, который экономит 2 часа в день"
]

def publish_video():
    """Публикует видео в каналы"""
    bot = telebot.TeleBot(BOT_TOKEN)
    
    video_url = random.choice(VIDEOS)
    caption = random.choice(CAPTIONS)
    
    for channel_id in CHANNELS:
        try:
            bot.send_video(chat_id=channel_id, video=video_url, caption=caption)
            print(f"✅ Видео опубликовано в {channel_id}")
        except Exception as e:
            print(f"❌ Ошибка в {channel_id}: {e}")

if __name__ == "__main__":
    publish_video()
