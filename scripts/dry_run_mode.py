from pathlib import Path
import loading_config_files
from logging_manager import LoggingManager


CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_CATEGORIES = loading_config_files.load_config_categories()

logger_ERROR = LoggingManager.get_logger('error_logger')
logger_INFO = LoggingManager.get_logger('only_info_console_logger')

path = Path(CONFIG_SETTINGS.get('watch_folder'))

def dry_run(conf_cat, path):
  list_file_path = file_enumerate(path)
  
  if list_file_path is None:
    logger_ERROR.error('Файлы не найдены, проверьте корректность ввода')
    return
  
  for path_file in list_file_path:
    extension = Path(path_file.name).suffix
    category_name = get_category_name(conf_cat, extension)
    
    if category_name is None:
      logger_ERROR.error(f'Название категории для расширения {extension} не найдено, проверьте наличие расширения в нужной категории')
      return
    
    print(f'Берем файл {path_file.name}, перемещает его из {Path(path_file.parent)} в директорию {Path(path) / category_name}')
  
  print('Сортировка завершена')

def get_category_name(conf_cat, extension):
  for rule in conf_cat.get('rules', []):
    if extension in rule.get('extension', []):
      return rule.get('category')
  
  return None

def file_enumerate(path):
  result_list_file_path = [file_path for file_path in path.rglob('*') if file_path.is_file()]
  
  if len(result_list_file_path) == 0:
    return None
  else:
    return result_list_file_path