import os
import random
import string
import shutil
from pathlib import Path
import loading_config_files


CONFIG_SETTINGS = loading_config_files.load_config_settings()

path = Path(CONFIG_SETTINGS.get("watch_folder"))


class TestFileGenerator:
    def __init__(self, base_dir=path):
        self.base_dir = Path(base_dir)
        # Очищаем и создаем тестовую директорию
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)
        self.base_dir.mkdir(parents=True)
        
        # Расширения для разных категорий
        self.extensions = {
            'images': ['.jpg', '.png', '.gif', '.bmp', '.tiff'],
            'documents': ['.txt', '.pdf', '.docx', '.xlsx', '.pptx', '.md'],
            'audio': ['.mp3', '.wav', '.flac', '.aac'],
            'video': ['.mp4', '.avi', '.mkv', '.mov'],
            'archives': ['.zip', '.rar', '.tar.gz', '.7z'],
            'code': ['.py', '.js', '.html', '.css', '.cpp', '.java'],
        }
        
    def create_dummy_file(self, filepath, size_kb=1, content_type='random'):
        """Создает файл с заданным содержимым"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        if content_type == 'text':
            # Текстовый файл
            with open(filepath, 'w') as f:
                f.write(''.join(random.choices(string.ascii_letters + string.digits, 
                                             k=size_kb * 1024)))
        elif content_type == 'binary':
            # Бинарный файл
            with open(filepath, 'wb') as f:
                f.write(os.urandom(size_kb * 1024))
        elif content_type == 'pdf_like':
            # Имитация PDF (начинается с %PDF)
            with open(filepath, 'wb') as f:
                f.write(b'%PDF-1.4\n')
                f.write(os.urandom(size_kb * 1024))
        elif content_type == 'jpg_like':
            # Имитация JPEG (начинается с FF D8)
            with open(filepath, 'wb') as f:
                f.write(b'\xFF\xD8\xFF\xE0')
                f.write(os.urandom(size_kb * 1024))
        else:
            # Случайное содержимое
            with open(filepath, 'wb') as f:
                f.write(os.urandom(size_kb * 1024))
    
    def generate_files(self, num_files=1000):
        """Генерирует указанное количество файлов"""
        print(f"Генерация {num_files} тестовых файлов...")
        
        for i in range(num_files):
            # Выбираем случайную категорию и расширение
            category = random.choice(list(self.extensions.keys()))
            ext = random.choice(self.extensions[category])
            
            # Генерируем случайное имя файла
            name_length = random.randint(5, 15)
            filename = ''.join(random.choices(string.ascii_lowercase + string.digits, 
                                             k=name_length))
            
            # Создаем поддиректории для разнообразия
            subdirs = random.randint(0, 2)
            filepath = self.base_dir
            for _ in range(subdirs):
                filepath = filepath / ''.join(random.choices(string.ascii_lowercase, k=5))
            
            filepath = filepath / f"{filename}{ext}"
            
            # Выбираем тип содержимого
            content_type = random.choice(['text', 'binary', 'pdf_like', 'jpg_like'])
            size = random.randint(1, 100)  # от 1КБ до 100КБ
            
            self.create_dummy_file(filepath, size_kb=size, content_type=content_type)
            
            if (i + 1) % 100 == 0:
                print(f"Создано {i + 1} файлов...")
        
        print(f"Готово! Создано {num_files} файлов в {self.base_dir}")
        
        # Возвращаем статистику
        return self.get_stats()
    
    def get_stats(self):
        """Возвращает статистику по созданным файлам"""
        stats = {cat: 0 for cat in self.extensions}
        total_size = 0
        
        for filepath in self.base_dir.rglob('*'):
            if filepath.is_file():
                ext = filepath.suffix.lower()
                total_size += filepath.stat().st_size
                
                for cat, exts in self.extensions.items():
                    if ext in exts:
                        stats[cat] += 1
                        break
                else:
                    stats.setdefault('other', 0)
                    stats['other'] += 1
        
        return {
            'total_files': sum(stats.values()),
            'total_size_mb': total_size / (1024 * 1024),
            'by_category': stats
        }

# Использование
if __name__ == "__main__":
    generator = TestFileGenerator(path)
    stats = generator.generate_files(100)
    print(f"\nСтатистика:")
    print(f"Всего файлов: {stats['total_files']}")
    print(f"Общий размер: {stats['total_size_mb']:.2f} МБ")
    print("По категориям:", stats['by_category'])