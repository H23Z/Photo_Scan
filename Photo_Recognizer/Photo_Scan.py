

 
   

import os
import io
from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

class ProductScanner:
    def __init__(self):
        """Инициализация клиента Vision API"""
        load_dotenv()  # Загружаем переменные окружения
        self.client = vision.ImageAnnotatorClient()

    def scan_product(self, image_path):
        """Основная функция сканирования продукта"""
        try:
            # Чтение изображения
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Распознавание текста (первая строка как название)
            text_response = self.client.text_detection(image=image)
            product_name = self._extract_product_name(text_response)
            
            # Распознавание штрих-кода
            barcode = self._detect_barcode(image)
            
            # Создание карточки
            card_path = self.create_product_card(product_name, barcode)
            
            return {
                'status': 'success',
                'product_name': product_name,
                'barcode': barcode,
                'card_path': card_path
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def _extract_product_name(self, response):
        """Извлекает первую строку текста как название продукта"""
        if not response.text_annotations:
            return "Название не найдено"
        return response.text_annotations[0].description.split('\n')[0]

    def _detect_barcode(self, image):
        """Обнаруживает штрих-код на изображении"""
        response = self.client.barcode_detection(image=image)
        if not response.barcode_annotations:
            return "Штрих-код не найден"
        return response.barcode_annotations[0].description

    def create_product_card(self, product_name, barcode, output_dir='output'):
        """Создает визуальную карточку продукта"""
        # Создаем папку для результатов, если ее нет
        os.makedirs(output_dir, exist_ok=True)
        
        # Создаем изображение карточки
        img = Image.new('RGB', (800, 400), color='white')
        draw = ImageDraw.Draw(img)
        
        # Пытаемся использовать красивый шрифт
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default(size=36)
        
        # Рисуем заголовок
        draw.text((50, 50), "КАРТОЧКА ПРОДУКТА", fill="black", font=font)
        
        # Добавляем информацию о продукте
        draw.text((50, 150), f"Название: {product_name}", fill="black", font=font)
        draw.text((50, 220), f"Штрих-код: {barcode}", fill="black", font=font)
        
        # Сохраняем карточку
        card_path = os.path.join(output_dir, 'product_card.png')
        img.save(card_path)
        
        return card_path

if __name__ == "__main__":
    # Инициализация сканера
    scanner = ProductScanner()
    
    # Получаем путь к изображению от пользователя
    image_path = input(r"C:\\Users\\HP\\Documents\\Visual Code\\Projects\\Photo Scan\\Image\\Sausage.jpg ").strip('"')
    
    # Обработка изображения
    result = scanner.scan_product(image_path)
    
    # Вывод результатов
    if result['status'] == 'success':
        print("\n" + "="*50)
        print(f"УСПЕШНО ОБРАБОТАНО!")
        print(f"Название: {result['product_name']}")
        print(f"Штрих-код: {result['barcode']}")
        print(f"Карточка сохранена: {result['card_path']}")
        print("="*50)
        
        # Показываем карточку
        try:
            Image.open(result['card_path']).show()
        except:
            print("Не удалось открыть изображение карточки")
    else:
        print("\nОШИБКА:", result['message'])