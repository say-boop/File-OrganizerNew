from pathlib import Path
import shutil
import main
from categories import FILE_CATEGORIES


def sorting_files_into_folders():
  path = main.find_folder_path()
  if path:
    list_files = [child.name for child in path.iterdir() if child.is_file()]
    if len(list_files) == 0:
      print('Файлы не найдены')
      sorting_files_into_folders()
  else:
    print('Папка не найден, проверьте корректность ввода.')
    sorting_files_into_folders()
  
  for file in list_files:
    str_file = Path(file)
    extension = str_file.suffix
    folder_name = search_folder_name(extension)
    result_path = path / folder_name
    
    if not result_path.is_dir():
      result_path.mkdir(parents=True, exist_ok=True)
    
    source = path / file
    shutil.move(source, result_path)

def search_folder_name(extension):
  for name_folder, extension_list in FILE_CATEGORIES.items():
    if extension in extension_list:
      return name_folder

sorting_files_into_folders()