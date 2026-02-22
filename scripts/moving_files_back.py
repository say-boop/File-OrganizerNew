from pathlib import Path
import loading_config_files
import shutil
import os

CONFIG_RESET = loading_config_files.load_config_reset()

path_from = []
path_to = []
file_size_before_B = []
file_modification_time_before = []
disk_size_full = 0

def get_info(config):
  for rule in config.get('file', []):
    global path_from
    path_from.append(rule.get('path_from'))
    path_to.append(rule.get('path_to'))
    file_size_before_B.append(rule.get('file_size_before_B'))
    file_modification_time_before.append(rule.get('file_modification_time_before'))
  
  global disk_size_full
  disk_size_full = sum([int(x) for x in file_size_before_B])

get_info(CONFIG_RESET)

def delete_folder(folder_path):
  files_and_folders_count = len([f for f in folder_path.iterdir()])
  
  if files_and_folders_count == 0:
    shutil.rmtree(folder_path)

def moving_files(path_from_arr, path_to_arr, file_size_before_arr, file_mod_time_before_arr):
  count = 0
  
  for _ in range(len(path_from_arr)):
    path_from = Path(path_from_arr[count])
    path_to = Path(path_to_arr[count])
    file_size_before = Path(file_size_before_arr[count])
    file_mod_time_before = Path(file_mod_time_before_arr[count])
    nested_folder = path_from.parent
    
    checking_file_modifications(path_to, file_size_before, file_mod_time_before)
    checking_dick_space(path_from, disk_size_full)
    
    if path_from.exists():
      count = 1
      while path_from.exists():
        new_name = f"{path_from.stem}_{count}{path_from.suffix}"
        path_from = path_from.parent / new_name
        count += 1
    
    if not nested_folder.is_dir():
      nested_folder.mkdir(parents=True, exist_ok=True)
    
    if Path(path_to).exists():
      shutil.move(path_to, path_from)
    count += 1
    
    delete_folder(Path(path_to).parent)

def checking_file_modifications(path_to, file_size_before, file_mod_time_before):
  file_size_now = Path(path_to).stat().st_size
  date_modified_now = Path(path_to).stat().st_mtime
  
  if file_size_before == file_size_now and file_mod_time_before == date_modified_now:
    print('Файл был изменен')

def checking_dick_space(path, disk_size_full):
  path_from = Path(path)
  disk_name = Path(path_from.drive)
  
  usage = shutil.disk_usage(disk_name)
  
  if not usage.free > disk_size_full:
    print('Нету необходимого количества места на диске')

moving_files(path_from, path_to, file_size_before_B, file_modification_time_before)