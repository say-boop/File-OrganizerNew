from pathlib import Path
import yaml

def load_config_settings():
  config_path = Path(__file__).parent.parent / "config" / "settings.yml"
  
  if not config_path.exists():
    create_def_conf(config_path)
    return change_config()
  
  with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
    return config

def change_config():
  print('Создан дефолтный конфиг файл.')
  print('Измените конфиг файл под свои нужды и заново запустите программу.')
  exit()

def load_config_categories():
  config_path = Path(__file__).parent.parent / "config" / "categories.yml"
  
  with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
    return config


# Шаблон создания дефолтного конфиг файла
def create_def_conf(config_path):
  default_content = f"""
# Какие папки сортировать
"watch_folder": {str(Path.cwd())}

# Режим предпросмотра: true = только смотрим, false = реально перемещаем
"dry_run": true

# Куда складывать отсортированное
"output_base": {str(Path.cwd())}
  """
  
  with open(config_path, 'w', encoding="utf-8") as f:
    f.write(default_content)