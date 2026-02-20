from pathlib import Path
import yaml
from logging_manager import LoggingManager

logger_ERROR = LoggingManager.get_logger('error_logger')
logger_INFO = LoggingManager.get_logger('only_info_console_logger')

def load_config_settings():
  config_path = Path(__file__).parent.parent / "config" / "settings.yml"
  
  if not config_path.exists():
    logger_ERROR.warning('Configuration file not found, default will be created')
    create_def_conf(config_path)
    return change_config()
  
  logger_INFO.info('The config file has been found')
  logger_INFO.info('Starting to download the config file')
  with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    logger_INFO.info('File uploaded successfully, good job')
    return config

def change_config():
  logger_INFO.info('A default configuration file has been created')
  logger_INFO.info('Change the configuration file to suit your needs and run the program again')
  exit()

def load_config_categories():
  config_path = Path(__file__).parent.parent / "config" / "categories.yml"
  
  logger_INFO.info('Configuration file with categories found')
  
  logger_INFO.info('Starting to download the config file')
  with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    logger_INFO.info('The category file has been uploaded')
    return config

def load_config_reset():
  config_path = Path(__file__).parent.parent / "config" / "recording_comp_actions.yml"
  
  logger_INFO.info('Configuration file with categories found')
  
  logger_INFO.info('Starting to download the config file')
  with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    logger_INFO.info('The category file has been uploaded')
    return config


# Шаблон создания дефолтного конфиг файла
def create_def_conf(config_path):
  default_content = f"""
# Какие папки сортировать
"watch_folder": {str(Path.cwd())}

# Режим предпросмотра: true = только смотрим, false = реально перемещаем
"dry_run": true

# Удаление отсортированных папок: true - да, false - нет
deleting_folders: true

# Путь до yml файла для записи об выполненных действиях.
recording_comp_actions: {str(Path.cwd())}
  """
  
  with open(config_path, 'w', encoding="utf-8") as f:
    f.write(default_content)