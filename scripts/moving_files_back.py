from pathlib import Path
import loading_config_files
import shutil
from logging_manager import LoggingManager
from ruamel.yaml import YAML
from tqdm import tqdm
import sys
import multiprocessing
from multiprocessing import Pool
from functools import partial
import os


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

def move_single_file(file_info, disk_size_full):
  src = file_info['src']
  dst = file_info['dst']
  
  checking_file_changes(src, file_info['timestamp'])
  checking_dick_space(dst, disk_size_full)
  
  dst_path = Path(dst)
  if not dst_path.parent.exists():
    dst_path.parent.mkdir(parents=True, exist_ok=True)
  
  if Path(src).exists():
    shutil.move(src, dst)
    return True
  return False

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
  
  files_to_move = []
  indexes_to_update = []
  
  for i in range(start_index, end_index):
    if passed_file[i]:
      add_one_to_conf_set()
      continue
    
    indexes_to_update.append(i)
    
    src_path = str(path_to_arr[i])
    dst_path = str(path_from_arr[i])
    timestamp = int(timestamp_file[i])
    
    if not Path(src_path).exists():
      logger_INFO.info(f'Файл {src_path} не найден')
      add_one_to_conf_set()
      continue
    
    files_to_move.append({
      'src': src_path,
      'dst': dst_path,
      'timestamp': timestamp
    })
  
  if files_to_move:
    move_func = partial(move_single_file, disk_size_full=disk_size_full)

    with Pool(processes=multiprocessing.cpu_count()) as pool:
      for _ in tqdm(pool.imap_unordered(move_func, files_to_move), total=len(files_to_move), desc='Rollback', unit='File'):
        pass
  
  for i in indexes_to_update:
    add_one_to_conf_set()
    change_the_state_of_passed_file(Path(path_to_arr[i]).name)
    
    source_folder = Path(path_to_arr[i]).parent
    try:
      if source_folder.exists() and len(list(source_folder.iterdir())) == 0:
        shutil.rmtree(source_folder)
    except Exception as e:
      logger_ERROR.error(f'Ошибка {e}')
    
  
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
  except Exception as e:
    logger_ERROR.error(f'Ошибка: {e}')

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
  except Exception as e:
    logger_ERROR.error(f'Ошибка: {e}')

def rollback_N_quantity():
  global CONFIG_SETTINGS
  CONFIG_SETTINGS = loading_config_files.load_config_settings()
  current_count = CONFIG_SETTINGS.get('passed_count', 0)
  
  user_response = int(input('Произвести откат по количеству файлов? (1/0): '))
  user_consent = int(input('Согласны откатить изменения? (1/0): '))
  
  if user_consent:
    if user_response:
      max_possible = len(passed_files) - current_count
      number_files = int(input('Введите количество файлов для отката: '))
    
      if number_files > max_possible:
        logger_INFO.info(f'Нельзя откатить больше чем {max_possible} файлов. Откатываем все оставшиеся')
        number_files = max_possible
    
      moving_files(path_from, path_to, file_timestamp, passed_files, number_files)
    else:
      moving_files(path_from, path_to, file_timestamp, passed_files)