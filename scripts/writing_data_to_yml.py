from pathlib import Path
from logging_manager import LoggingManager
import loading_config_files

logger_ERROR = LoggingManager.get_logger('error_logger')
logger_INFO = LoggingManager.get_logger('only_info_console_logger')

CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_RESET = loading_config_files.load_config_reset()

path_recording_comp_actions = Path(CONFIG_SETTINGS.get("recording_comp_actions"))

def check_file_presence_recording_comp_actions(config_set):
  path_file = Path(config_set.get("recording_comp_actions"))
  logger_INFO.info('File found')
  
  if path_file.exists():
    return True
  else:
    logger_ERROR.warning('The file for writing data is missing and will be recreated')
    create_def_config(path_file)

def create_def_config(config_path):
  default_message = """file:"""
  
  with open(config_path, 'w', encoding='utf-8') as f:
    f.write(default_message)

def reading_conf_file(config_rec_comp_actions, message):
  with open(config_rec_comp_actions, 'a', encoding='utf-8') as f:
    f.write(message)

def result_message(path_from, path_to, filename, file_size_before, file_timestamp, passed=False):
  input_message = f"""
  - filename: '{filename}'
    path_from: '{path_from}'
    path_to: '{path_to}'
    file_size_before_B: '{file_size_before}'
    timestamp_before: '{file_timestamp}'
    passed: {passed}
"""
  reading_conf_file(path_recording_comp_actions, input_message)

def overwriting_file_when_sorting_again(config_rec_comp_act):
  message = f"""file:"""
  with open(config_rec_comp_act, 'w', encoding='utf-8') as f:
    f.write(message)