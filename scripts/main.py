import click
import creating_folder_and_sort_files
import loading_config_files
from pathlib import Path
import dry_run_mode
import moving_files_back

CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_CATEGORIES = loading_config_files.load_config_categories()

path = Path(CONFIG_SETTINGS.get("watch_folder"))
path_recording_comp_actions = Path(CONFIG_SETTINGS.get("recording_comp_actions"))


@click.group()
def cli():
  pass

@cli.command()
def regularSort():
  """
  Обычная сортировка файлов.
  
  \b
  Описание:
    Команда сортирует файлы в директории выбранной в конфигурационном файле,
    распределяя их по папка в зависимости от расширения. 
    (вложенные папки не сортирует)
  
  \b
  Алгоритм работы:
    1. Сканируется текущая папка
    2. Определяется расширение файла и имя папки для перемещения
    3. Создается папка (если её нет)
    4. Перемещение файлов в соответствующие папки
  
  \b
  Пример работы: 
    Было:                   Стало:
    report.pdf    ->        Documents/report.pdf
    photo.jpg    ->        Images/photo.jpg
    song.mp3    ->        Audio/song.mp3
  
  \b
  Пример:
    python main.py regularsort
    python main.py regularsort --help
  
  \b
  Примечание:
    Файлы с неизвестными расширениями перемещаются в папку other, 
    по желанию можно добавить в файл categories.yml это расширения под 
    нужную категорию.
  """
  click.echo('Запуск обычной сортировки')
  creating_folder_and_sort_files.regular_sort(path, CONFIG_CATEGORIES)

@cli.command()
def recursiveSort():
  """
  Рекурсивная сортировка файлов.
  
  \b
  Описание:
    Команда рекурсивно обходт все папки и сортирует файлы в директории 
    выбранной в конфигурационном файле,распределяя их по папкам
    в зависимости от расширения. (вложенные папки не сортирует)
  
  \b
  Отличие от обычной сортировки:
    - Проверяет все подпапки
    - Сохраняет относительные пути
    - Требует больше времени
  
  \b
  Пример:
    python main.py recursivesort
    python main.py recursivesort --help
  
  \b
  Примечание:
    Файлы с неизвестными расширениями перемещаются в папку other, 
    по желанию можно добавить в файл categories.yml это расширения под 
    нужную категорию.
  
  \b
  Внимание!
    Не рекомендуется запускать в системных папках
    Сделайте резервную копию важных данных
    Для теста сначала запустите режим dry-run:
      python main.py dry-run
  """
  click.echo('Запуск рекурсивной сортировки')
  creating_folder_and_sort_files.recursive_sort(path)

@cli.command()
def dry_run():
  """
  Режим предпросмотра сортировки.
  
  \b
  Описание:
    Команда показывает как будет сортировать программа
    без настоящего перемещения.
  
  \b
  Пример:
    python main.py dry-run
    python main.py dry-run --help
  """
  dry_run_mode.dry_run(CONFIG_CATEGORIES, path)

@cli.command()
def moving_back():
  """
  Откатывает сортировки и возвращает всё как было.
  
  \b
  Описание:
    Команда возвращает файлы ка кони были до сортировки.
    Также можно откатывать файлы частями, допустим сначала 50,
    потом позже еще 50.
  
  \b
  Пример:
    python main.py moving-back
    python main.py moving-back --help
  """
  pass
  moving_files_back.rollback_N_quantity()

if __name__ == "__main__":
  cli()