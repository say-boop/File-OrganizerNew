from pathlib import Path
import shutil
import loading_config_files


CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_CATEGORIES = loading_config_files.load_config_categories()


def creating_folders_and_sort_files(config_set, config_categor):
  path = Path(config_set.get("watch_folder"))
  recursively = int(input('Произвести сортировку всех вложенных папок (1/0): '))
  if not recursively:
    list_files = regular_sort(path)
  else:
    list_files = recursive_sort(path)
  
  for file in list_files:
    str_file = Path(file)
    extension = str_file.suffix
    folder_name = get_category_name(config_categor, extension)
    if folder_name is None:
      print(f'Для расширеня {extension} не найдена категория')
      folder_name = "other"
    
    result_path = path / folder_name
    
    if not result_path.is_dir():
      result_path.mkdir(parents=True, exist_ok=True)
    
    source = path / file
    shutil.move(source, result_path)

def get_category_name(config, target_ext):
  for rule in config.get('rules', []):
    if target_ext in rule.get('extension', []):
      return rule.get('category')
  
  return None


def regular_sort(path):
  if path:
    list_files = [item.name for item in path.iterdir() if item.is_file()]
  else:
    print('Папка не найдена, проверьте корректность ввода')
    creating_folders_and_sort_files()
  
  return list_files

def recursive_sort(path):
  result_file = []
  name_folders = []
  if path:
    list_files_folders = [item.name for item in path.iterdir()]
  else:
    print('Папка не найдена, проверьте корректность ввода')
    creating_folders_and_sort_files()
  
  for item in list_files_folders:
    str_file = Path(item)
    
    if not str_file.suffix:
      path_dir = path / item
      name_folders.append(item)
      
      list_nested_files = [file.name for file in path_dir.iterdir()]
      for file in path_dir.iterdir():
        source = path_dir / file
        shutil.move(source, path)
      result_file.extend(list_nested_files)
    else:
      result_file.append(item)
  
  deleting_folders(path, name_folders)
  
  return result_file

def deleting_folders(path, name_folders):
  if len(name_folders) <= 0:
    return None
  
  print(f'Список отсортированных папок: {name_folders}')
  del_folder = int(input('Хотите ли вы удалить папки (1/0): '))
  
  if del_folder:
    for folder in name_folders:
      path_dir = path / folder
      if any(path_dir.iterdir()):
        delete_with_files = int(input('В папке есть файлы, всё равно удалить? (1/0): '))
        if delete_with_files:
          shutil.rmtree(path_dir)
      else:
        shutil.rmtree(path_dir)
  else:
    return None

creating_folders_and_sort_files(CONFIG_SETTINGS, CONFIG_CATEGORIES)