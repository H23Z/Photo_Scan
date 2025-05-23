import os
import io
from dotenv import load_dotenv  # Добавлено!
from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont

class ProductScanner:
    def __init__(self):
        """Инициализация с загрузкой .env"""
        load_dotenv()  # Загружаем переменные из .env
        self.client = vision.ImageAnnotatorClient()  # Автоматически использует GOOGLE_APPLICATION_CREDENTIALS

    # ... (остальные методы без изменений)

if __name__ == "__main__":
    # Проверяем, загрузился ли ключ (дополнительная валидация)
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Ошибка: Не найден путь к ключу в .env файле!")
        print("Создайте файл .env с содержимым:")
        print('GOOGLE_APPLICATION_CREDENTIALS="C:\\Users\\HP\\Documents\\Visual Code\\Projects\\Photo Scan\\Photo Scan\\Vision Key.json"')
        exit(1)