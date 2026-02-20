from pathlib import Path
import loading_config_files

CONFIG_RESET = loading_config_files.load_config_reset()

path_from = ''

def get_c(config):
  for rule in config.get('file', []):
    global path_from
    path_from = rule.get('path_from')
    return

get_c(CONFIG_RESET)

print(path_from)