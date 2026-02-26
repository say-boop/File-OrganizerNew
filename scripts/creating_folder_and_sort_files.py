from pathlib import Path
import shutil
import loading_config_files
from logging_manager import LoggingManager
import writing_data_to_yml
from tqdm import tqdm
import sys

logger_ERROR = LoggingManager.get_logger('error_logger')
logger_INFO = LoggingManager.get_logger('only_info_console_logger')

CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_CATEGORIES = loading_config_files.load_config_categories()

writing_data_to_yml.check_file_presence_recording_comp_actions(CONFIG_SETTINGS)

path = Path(CONFIG_SETTINGS.get("watch_folder"))
path_recording_comp_actions = Path(CONFIG_SETTINGS.get("recording_comp_actions"))


def regular_sort(path, config_cat):
  path_dir = Path(path)
  
  writing_data_to_yml.overwriting_file_when_sorting_again(path_recording_comp_actions)
  
  if not path_dir:
    logger_ERROR.error('The path is incorrect, check the configuration file, field "watch_folder"')
  
  progress_bar = tqdm(
    total=(len([f for f in path.iterdir()])),
    desc="Copying",
    file = sys.stdout,
    miniters=1,
    ascii=True
  )
  
  for path_file in path.iterdir():
    file = Path(path_file)
    extension = file.suffix
    folder_name = get_category_name(config_cat, extension)
    
    if folder_name is None:
      logger_INFO.info(f'Category not found for {extension} extension')
      folder_name = "other"
    
    result_path = path_dir / folder_name
    final_path = result_path / file.name
    file_size = file.stat().st_size
    file_timestamp = int(file.stat().st_mtime)
    
    if not result_path.is_dir():
      result_path.mkdir(parents=True, exist_ok=True)
    
    writing_data_to_yml.result_message(file, final_path, file.name, file_size, file_timestamp)
    
    shutil.move(file, final_path)
    
    progress_bar.update(1)
  
  progress_bar.close()


def recursive_sort(path):
  base_path = Path(path)
  if not base_path.exists():
    logger_ERROR.error('Folder not found, check the configuration file to see if the path is correct')
    return
  
  writing_data_to_yml.overwriting_file_when_sorting_again(path_recording_comp_actions)
  
  all_files = [f for f in base_path.rglob('*') if f.is_file()]
  
  progress_bar = tqdm(
    total=(len([f for f in path.iterdir()])),
    desc="Copying",
    file = sys.stdout,
    miniters=1,
    ascii=True
  )
  
  if len(all_files) == 0:
    logger_ERROR.error('There are no files to sort in the folder, check the path')
    return
  
  for file in all_files:
    check_and_move(path, file)
    progress_bar.update(1)
  
  progress_bar.close()
  
  if CONFIG_SETTINGS.get("deleting_folders"):
    delete_folder(base_path)

def check_and_move(path, file_path):
  path_file = Path(file_path)
  path_dir = Path(path)
  
  if not path_dir:
    logger_ERROR.error('The path is incorrect, check the configuration file, field "watch_folder"')
  
  extension = path_file.suffix
  folder_name = get_category_name(CONFIG_CATEGORIES, extension)
  if folder_name is None:
    logger_INFO.info(f'Category not found for {extension} extension')
    folder_name = "other"
  
  result_path = path_dir / folder_name
  final_path_filename = result_path / path_file.name
  file_size = path_file.stat().st_size
  file_timestamp = int(path_file.stat().st_mtime)
  
  if final_path_filename.exists():
    count = 1
    while final_path_filename.exists():
      new_name = f"{path_file.stem}_{count}{path_file.suffix}"
      final_path_filename = result_path / new_name
      count += 1
    writing_data_to_yml.result_message(path_file, final_path_filename, new_name, file_size, file_timestamp)
  else:
    writing_data_to_yml.result_message(path_file, final_path_filename, path_file.name, file_size, file_timestamp)
  
  if not result_path.is_dir():
    result_path.mkdir(parents=True, exist_ok=True)
  
  
  shutil.move(path_file, final_path_filename)

def delete_folder(base_path):
  try:
    for folder in sorted(base_path.rglob('*'), key=lambda x: str(x), reverse=True):
      if folder.is_dir() and folder != base_path:
        try:
          contents = list(folder.iterdir())
          if len(contents) == 0:
            shutil.rmtree(folder)
            logger_INFO.info(f'Deleted empty folder: {folder}')
        except (PermissionError, FileNotFoundError) as e:
          logger_ERROR.error(f'Error accessing folder {folder}: {e}')
        except Exception as e:
          logger_ERROR.error(f'Error deleting folder {folder}: {e}')
  except Exception as e:
    logger_ERROR.error(f'Error during folder cleanup: {e}')

def get_category_name(conf_cat, target_ext):
  for rule in conf_cat.get('rules', []):
    if target_ext in rule.get('extension', []):
      return rule.get('category')
  
  return None


recursive_sort(path)