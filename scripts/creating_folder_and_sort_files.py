from pathlib import Path
import shutil
import loading_config_files
from logging_manager import LoggingManager
import writing_data_to_yml
import math


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
  
  for file in path.iterdir():
    extension = file.suffix
    folder_name = get_category_name(config_cat, extension)
    
    if folder_name is None:
      logger_INFO.info(f'Category not found for {extension} extension')
      folder_name = "other"
    
    result_path = path_dir / folder_name
    final_path = result_path / file.name
    file_size = math.ceil(file.stat().st_size / 1024)
    
    if not result_path.is_dir():
      result_path.mkdir(parents=True, exist_ok=True)
    
    writing_data_to_yml.result_message(file.name, file, final_path, "None", file_size)
    
    shutil.move(file, final_path)


def recursive_sort(path):
  base_path = Path(path)
  if not base_path.exists():
    logger_ERROR.error('Folder not found, check the configuration file to see if the path is correct')
    return
  
  writing_data_to_yml.overwriting_file_when_sorting_again(path_recording_comp_actions)
  
  all_files = [f for f in base_path.rglob('*') if f.is_file()]
  
  if len(all_files) == 0:
    logger_ERROR.error('There are no files to sort in the folder, check the path')
    return
  
  for file in all_files:
    check_and_move(path, file, CONFIG_CATEGORIES)

def check_and_move(path, file_path, config_cat):
  path_file = Path(file_path)
  path_dir = Path(path)
  
  if not path_dir:
    logger_ERROR.error('The path is incorrect, check the configuration file, field "watch_folder"')
  
  extension = path_file.suffix
  folder_name = get_category_name(config_cat, extension)
  if folder_name is None:
    logger_INFO.info(f'Category not found for {extension} extension')
    folder_name = "other"
  
  result_path = path_dir / folder_name
  final_path_filename = result_path / path_file.name
  file_size = math.ceil(path_file.stat().st_size / 1024)
  
  if final_path_filename.exists():
    count = 1
    while final_path_filename.exists():
      new_name = f"{path_file.stem}_{count}{path_file.suffix}"
      final_path_filename = result_path / new_name
      count += 1
    writing_data_to_yml.result_message(path_file.name, path_file, final_path_filename, new_name, file_size)
  else:
    writing_data_to_yml.result_message(path_file.name, path_file, final_path_filename, "None", file_size)
  
  if not result_path.is_dir():
    result_path.mkdir(parents=True, exist_ok=True)
  
  
  shutil.move(path_file, final_path_filename)
  
  delete_folder(path_file.parent, path_dir)

def delete_folder(folder, source_folder):
  files_and_folders_count = len([f for f in folder.iterdir()])
  
  if files_and_folders_count == 0:
    if not folder == source_folder:
      if CONFIG_SETTINGS.get("deleting_folders"):
        shutil.rmtree(folder)


def get_category_name(config, target_ext):
  for rule in config.get('rules', []):
    if target_ext in rule.get('extension', []):
      return rule.get('category')
  
  logger_INFO.warning('No category found for this extension.')
  return None


regular_sort(path, CONFIG_CATEGORIES)