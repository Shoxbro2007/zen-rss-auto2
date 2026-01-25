import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import random
import os

def create_video_from_image(text, duration=10):
    """Создает короткое видео из изображения с текстом"""
    
    # Создаем изображение с текстом
    img = Image.new('RGB', (1280, 720), color='black')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Разбиваем текст на строки
    lines = []
    words = text.split()
    line = ""
    
    for word in words:
        test_line = line + " " + word if line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] < 1000:  # Если строка помещается
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    
    # Рисуем текст по центру
    y_offset = 300
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1280 - text_width) // 2
        draw.text((x, y_offset), line, font=font, fill='white')
        y_offset += 60
    
    # Сохраняем изображение
    temp_img = "temp_frame.png"
    img.save(temp_img)
    
    # Создаем видео из изображения
    video_filename = f"generated_video_{random.randint(1000, 9999)}.mp4"
    
    # Используем ffmpeg для создания видео
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', temp_img,
        '-c:v', 'libx264',
        '-t', str(duration),
        '-pix_fmt', 'yuv420p',
        '-vf', 'scale=1280:720',
        video_filename
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Удаляем временные файлы
    os.remove(temp_img)
    
    return video_filename

def generate_video_post():
    """Генерирует видео с описанием"""
    descriptions = [
        "🔥 Искусственный интеллект меняет мир: как ИИ может сэкономить вам 3 часа в день",
        "💡 Как автоматизировать рутину: 5 инструментов, которые сократят вашу работу в 2 раза", 
        "🚀 Бизнес в 2026 году: как заработать 50 000 ₽ за 1 месяц, просто автоматизировав продажи",
        "💰 Финансовая свобода: как инвестировать 10 000 ₽ и удвоить их за 2 месяца",
        "🤖 Автоматизация в действии: Zapier, который экономит 2 часа в день"
    ]
    
    text = random.choice(descriptions)
    video_file = create_video_from_image(text, duration=15)
    
    return video_file, text

if __name__ == "__main__":
    video, caption = generate_video_post()
    print(f"✅ Видео создано: {video}")
    print(f"📝 Описание: {caption}")
