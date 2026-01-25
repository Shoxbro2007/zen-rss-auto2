import telebot
import os
import random
from datetime import datetime
from video_generator import generate_video_post

# 🔑 НАСТРОЙКИ
BOT_TOKEN = "8493219513:AAEm-pIf7SV-fALnSN5-hSi9BrRf39ayIT0"  # ЗАМЕНИТЬ!
CHANNELS = [
    "@tech_videos",
    "@business_videos", 
    "@finance_videos"
]

def publish_to_telegram():
    """Публикует СГЕНЕРИРОВАННОЕ видео в Telegram каналы"""
    
    bot = telebot.TeleBot(BOT_TOKEN)
    
    # Генерируем видео
    video_file, caption = generate_video_post()
    
    success_count = 0
    
    for channel in CHANNELS:
        try:
            # Публикуем видео
            with open(video_file, 'rb') as video:
                bot.send_video(
                    chat_id=channel,
                    video=video,
                    caption=caption,
                    supports_streaming=True
                )
            
            print(f"✅ Видео опубликовано в {channel}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Ошибка публикации в {channel}: {e}")
    
    # Удаляем сгенерированное видео
    if os.path.exists(video_file):
        os.remove(video_file)
    
    print(f"🚀 Успешно опубликовано в {success_count} из {len(CHANNELS)} каналов")

if __name__ == "__main__":
    publish_to_telegram()
