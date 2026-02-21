from pathlib import Path
import loading_config_files
import shutil

CONFIG_RESET = loading_config_files.load_config_reset()

path_from = []
path_to = []

def get_info(config):
  for rule in config.get('file', []):
    global path_from
    path_from.append(rule.get('path_from'))
    path_to.append(rule.get('path_to'))

get_info(CONFIG_RESET)

def delete_folder(folder_path):
  files_and_folders_count = len([f for f in folder_path.iterdir()])
  
  if files_and_folders_count == 0:
    shutil.rmtree(folder_path)

def moving_files(path_from_arr, path_to_arr):
  count = 0
  
  for _ in range(len(path_from_arr)):
    path_from = path_from_arr[count]
    path_to = path_to_arr[count]
    nested_folder = Path(path_from).parent
    
    if not nested_folder.is_dir():
      nested_folder.mkdir(parents=True, exist_ok=True)
    
    shutil.move(path_to, path_from)
    count += 1
    
    delete_folder(Path(path_to).parent)

moving_files(path_from, path_to)