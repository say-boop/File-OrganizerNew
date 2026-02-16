from pathlib import Path
import shutil
import loading_config_files


CONFIG_SETTINGS = loading_config_files.load_config_settings()
CONFIG_CATEGORIES = loading_config_files.load_config_categories()


def creating_folders_and_sort_files(config_set, config_categor):
  path = Path(config_set.get("watch_folder"))
  recursively = int(input('Произвести сортировку всех вложенных папок (1/0): '))
  if not recursively:
    regular_sort(path)
  else:
    recursive_sort(path)
  
  for file in path.iterdir():
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
  if not path:
    print('Папка не найдена, проверьте корректность ввода')
    creating_folders_and_sort_files()

def check_and_move(file_path, target_dir):
    file_path = Path(file_path)
    target_dir = Path(target_dir)
    
    final_path = target_dir / file_path.name
    
    if file_path.parent == target_dir and file_path.name == final_path.name:
        return file_path

    if final_path.exists():
        count = 1
        while final_path.exists():
            new_name = f"{file_path.stem}_{count}{file_path.suffix}"
            final_path = target_dir / new_name
            count += 1
            
    target_dir.mkdir(parents=True, exist_ok=True)
    return shutil.move(str(file_path), str(final_path))

def recursive_sort(path):
  base_path = Path(path)
  if not base_path.exists():
    print("Папка не найдена")
    return
  
  all_files = [f for f in base_path.rglob('*') if f.is_file()]
  
  for file in all_files:
    check_and_move(file, base_path)
    
  if CONFIG_SETTINGS.get("deleting_folders"):
    for subfolder in sorted([d for d in base_path.iterdir() if d.is_dir()], reverse=True):
      try:
        shutil.rmtree(subfolder)
      except Exception as e:
        print(f"Не удалось удалить {subfolder}: {e}")
    
  return all_files

creating_folders_and_sort_files(CONFIG_SETTINGS, CONFIG_CATEGORIES)