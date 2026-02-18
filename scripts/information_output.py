# В этом файле будет режим dry-run, пока его не делал, но в скоре возьмусь за него.

from pathlib import Path
import loading_config_files

CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_CATEGORIES = loading_config_files.load_config_categories()


def list_all_files():
  directory = Path(CONFIG_SETTINGS.get("watch_folder"))
  if directory:
    all_items = [child.name for child in directory.iterdir()]
  else:
    print('Папка не найден, проверьте корректность ввода.')
    list_all_files()
  
  files_only = []
  
  for item in all_items:
    full_path = directory / item
    if Path.is_file(full_path):
      files_only.append(item)
  
  return files_only

def counting_files_type(lst_files: list) -> dict:
  count_files = {}
  
  for file in lst_files:
    str_file = Path(file)
    extension = str_file.suffix
    
    if extension:
      name_categories = get_category_name(CONFIG_CATEGORIES, extension)
      
      if name_categories not in count_files:
        count_files[name_categories] = {}
      
      if extension not in count_files[name_categories]:
        count_files[name_categories][extension] = 0
      count_files[name_categories][extension] += 1
  
  return count_files

def get_category_name(config, target_ext):
  for rule in config.get('rules', []):
    if target_ext in rule.get('extension', []):
      return rule.get('category')
  
  return None

COUNT_FILES_TYPE = counting_files_type(list_all_files())

def dict_of_file_endings(folder_name: str, value_content: int):
  dict_file_endings = {
    '1': f'Я создам папку {folder_name} и перемещу туда {value_content} файл.',
    '2-4': f'Я создам папку {folder_name} и перемещу туда {value_content} файла.',
    '>5': f'Я создам папку {folder_name} и перемещу туда {value_content} файлов.'
  }
  
  return dict_file_endings

def determing_the_end_of_a_sentence_for_interence(folder_name: str, value_content: int):
  if value_content == 1:
    print(dict_of_file_endings(folder_name, value_content)['1'])
  elif 2 <= value_content <= 4:
    print(dict_of_file_endings(folder_name, value_content)['2-4'])
  else:
    print(dict_of_file_endings(folder_name, value_content)['>5'])

def dry_run(dict_count_files_type: dict):
  dict_folder = {}
  
  for name_folder, content in dict_count_files_type.items():
    count_content = sum([x for x in content.values()])
    dict_folder[name_folder] = count_content
  
  for folder_name, value_content in dict_folder.items():
    determing_the_end_of_a_sentence_for_interence(folder_name, value_content)

def file_sorting_work_plan(dict_count_files_type: dict):
  files_and_folders_to_sort = {}
  list_output = {folder_name: value_content for folder_name, value_content in dict_count_files_type.items()}
  
  for key, value in COUNT_FILES_TYPE.items():
    print(f'{key}: {value}')
  print('=' * 100)
  
  while True:
    for folder_name, content in list_output.items():
      print(f'Я создам папку {folder_name} и перемещу туда этот список файлов: {content}.')
      user_consent = input('Согласны перенести? (yes/no): )').lower()
      if user_consent == 'yes' or user_consent == 'y':
        files_and_folders_to_sort[folder_name] = content
        print('Добавлено в список для сортировки.')
        print('*' * 100)
      else:
        print('Не добавляем в список для сортировки.')
        print('*' * 100)
    print(files_and_folders_to_sort)
    break

file_sorting_work_plan(COUNT_FILES_TYPE)