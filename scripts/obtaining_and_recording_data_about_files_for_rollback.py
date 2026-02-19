from pathlib import Path
from logging_manager import LoggingManager
import loading_config_files

logger_ERROR = LoggingManager.get_logger('error_logger')
logger_INFO = LoggingManager.get_logger('only_info_console_logger')

CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_RESET = loading_config_files.load_config_reset()

def check_file_presence_recording_comp_actions(config_set):
  path_file = Path(config_set.get("recording_comp_actions"))
  logger_INFO.info('File found')
  
  if path_file.exists():
    return True
  else:
    logger_ERROR.warning('The file for writing data is missing and will be recreated')
    create_def_config(path_file)

path_recording_comp_actions = Path(CONFIG_SETTINGS.get("recording_comp_actions"))

def create_def_config(config_path):
  default_message = """"""
  
  with open(config_path, 'w', encoding='utf-8') as f:
    f.write(default_message)

def reading_conf_file(config_rec_comp_actions, message):
  with open(config_rec_comp_actions, 'a', encoding='utf-8') as f:
    f.write(message)

filename_var = []
path_from_var = []
path_to_var = []
file_size_before_var = []
file_size_after_var = []

def result_message(count):
  input_message = f"""file {filename_var[count]}:
  - filename: '{filename_var[count]}'
  - path_from: '{path_from_var[count]}'
  - path_to: '{path_to_var[count]}'
  - file_size_before_KB: '{file_size_before_var[count]}'
  - file_size_after_KB: '{file_size_after_var[count]}'
"""
  reading_conf_file(path_recording_comp_actions, input_message)
  

def get_filename(file_name):
  global filename_var
  filename_var.append(file_name)

def get_path_from_and_file_size_before(file_path, file_size):
  global path_from_var
  global file_size_before_var 
  path_from_var.append(file_path)
  file_size_before_var.append(file_size)

def get_path_to_and_file_size_after(result_path, file_size):
  global path_to_var
  global file_size_after_var
  path_to_var.append(result_path)
  file_size_after_var.append(file_size)