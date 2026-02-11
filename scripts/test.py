from pathlib import Path
import yaml
import creating_config_file

def load_config():
  config_path = Path(__file__).parent.parent / "config" / "sett.yml"
  
  if not config_path.exists():
    creating_config_file.create_def_conf(config_path)
    return change_config()
  
  with open(config_path, 'r', encoding="utf-8") as f:
    config = yaml.safe_load(f)
    return config

def change_config():
  print('Создан дефолтный конфиг файл.')
  print('Измените конфиг файл под свои нужды и заново запустите программу.')
  exit()

DATA_CONFIG = load_config()

def get_category_name(config, target_ext):
  for rule in config.get('rules', []):
    if target_ext in rule.get('extension', []):
      return rule.get('category')
  
  return None

# print(get_category_name(DATA_CONFIG, '.ovf'))