from pathlib import Path
import loading_config_files
import shutil
from logging_manager import LoggingManager
from ruamel.yaml import YAML


CONFIG_RESET = loading_config_files.load_config_reset()
CONFIG_SETTINGS = loading_config_files.load_config_settings()


logger_ERROR = LoggingManager.get_logger('error_logger')
logger_INFO = LoggingManager.get_logger('only_info_console_logger')


path_from = []
path_to = []
file_size_before_B = []
file_timestamp = []
passed_files = []
disk_size_full = 0
count_passed_true = [x for x in passed_files if x]


def get_info(config):
  for rule in config.get('file', []):
    path_from.append(rule.get('path_from'))
    path_to.append(rule.get('path_to'))
    file_size_before_B.append(rule.get('file_size_before_B'))
    file_timestamp.append(rule.get('timestamp_before'))
    passed_files.append(rule.get('passed'))
  
  global disk_size_full
  disk_size_full = sum([int(x) for x in file_size_before_B])

get_info(CONFIG_RESET)

def moving_files(path_from_arr, path_to_arr, timestamp_file, passed_file, rollback_N_quantity=None):
  global CONFIG_SETTINGS
  CONFIG_SETTINGS = loading_config_files.load_config_settings()
  current_point = CONFIG_SETTINGS.get('passed_count', 0)
  
  if current_point >= len(passed_file):
    add_one_to_conf_set(True)
    current_point = 0
  
  start_index = current_point
  
  if rollback_N_quantity is not None:
    end_index = start_index + rollback_N_quantity
  else:
    end_index = len(passed_file)
  
  if end_index > len(passed_file):
    end_index = len(passed_file)
  
  if start_index >= end_index:
    return
  
  for i in range(start_index, end_index):
    if passed_file[i]:
      add_one_to_conf_set()
      continue
  
    path_from = Path(path_from_arr[i])
    path_to = Path(path_to_arr[i])
    file_timestamp_before = int(timestamp_file[i])
    nested_folder = path_from.parent
  
    if not path_to.exists():
      logger_INFO.info(f'Файл {path_to} не найден')
      add_one_to_conf_set()
      continue
    
    checking_dick_space(path_from, disk_size_full)
    checking_file_changes(path_to, file_timestamp_before)
    
    if path_from.exists():
      counter = 1
      temp_path_from = path_from
      while temp_path_from.exists():
        new_name = f"{path_from.stem}_{counter}{path_from.suffix}"
        temp_path_from = path_from.parent / new_name
        counter += 1
      path_from = temp_path_from
    
    if not nested_folder.exists():
      nested_folder.mkdir(parents=True, exist_ok=True)
    
    if path_to.exists():
      shutil.move(str(path_to), str(path_from))
    
    change_the_state_of_passed_file(path_to.name)
    
    source_folder = path_to.parent
    try:
      if source_folder.exists() and len(list(source_folder.iterdir())) == 0:
        shutil.rmtree(source_folder)
    except:
      pass
    
    add_one_to_conf_set()
  
  CONFIG_SETTINGS = loading_config_files.load_config_settings()
  new_count = CONFIG_SETTINGS.get('passed_count', 0)
  
  if new_count >= len(passed_file):
    add_one_to_conf_set(True)

def add_one_to_conf_set(reset=False):
  config_path = Path(__file__).parent.parent / "config" / "settings.yml"
  
  yaml = YAML()
  yaml.preserve_quotes = True
  yaml.indent(mapping=2, sequence=4, offset=2)
  yaml.width = 4096
  
  try:
    with open(config_path, 'r', encoding='utf-8') as f:
      data = yaml.load(f)
  
    if reset:
      data['passed_count'] = 0
    else:
      data['passed_count'] += 1
  
    with open(config_path, 'w', encoding='utf-8') as f:
      yaml.dump(data, f)
  except:
    pass

def delete_folder(folder_path):
  if folder_path.exists() and folder_path.is_dir():
    files_and_folders_count = len([f for f in folder_path.iterdir()])
    
    if files_and_folders_count == 0:
      shutil.rmtree(folder_path)

def checking_file_changes(path_to, timestamp_before):
  path_file = Path(path_to)
  if path_file.exists():
    file_timestamp_after = int(path_file.stat().st_mtime)
  
    if file_timestamp_after > timestamp_before:
      logger_INFO.info('The file was modified after sorting')

def checking_dick_space(path, disk_size_full):
  path_from = Path(path)
  disk_name = Path(path_from.drive)
  
  usage = shutil.disk_usage(disk_name)
  
  if not usage.free > disk_size_full:
    logger_INFO.info('There is not enough disk space')

def change_the_state_of_passed_file(filename):
  config_path = Path(__file__).parent.parent / "config" / "recording_comp_actions.yml"
  
  yaml = YAML()
  yaml.preserve_quotes = True
  yaml.indent(mapping=2, sequence=4, offset=2)
  yaml.width = 4096
  
  try:
    with open(config_path, 'r', encoding='utf-8') as f:
      data = yaml.load(f)
    
    if 'file' in data and isinstance(data['file'], list):
      for item in data['file']:
        if item.get('filename') == filename:
          item['passed'] = True
    
    with open(config_path, 'w', encoding='utf-8') as f:
      yaml.dump(data, f)
  except:
    pass

def rollback_N_quantity():
  global CONFIG_SETTINGS
  CONFIG_SETTINGS = loading_config_files.load_config_settings()
  current_count = CONFIG_SETTINGS.get('passed_count', 0)
  
  user_response = int(input('Произвести откат по количеству файлов? (1/0): '))
  
  if user_response:
    max_possible = len(passed_files) - current_count
    number_files = int(input('Введите количество файлов для отката: '))
    
    if number_files > max_possible:
      logger_INFO.info(f'Нельзя откатить больше чем {max_possible} файлов. Откатываем все оставшиеся')
      number_files = max_possible
    
    moving_files(path_from, path_to, file_timestamp, passed_files, number_files)
  else:
    moving_files(path_from, path_to, file_timestamp, passed_files)

rollback_N_quantity()