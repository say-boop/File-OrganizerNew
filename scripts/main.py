from pathlib import Path
from categories import FILE_CATEGORIES

def list_all_files():
  directory = find_folder_path()
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

def find_folder_path():
  disk = input('Введите название диска в правильном формате (Пример: E:/): ')
  folder_name = input('Введите название папки: ')
  
  for folder in Path(disk).rglob(f'**/{folder_name}/'):
    if folder.is_dir():
      return folder.absolute()
  
  return None

def counting_files_type(lst_files: list) -> dict:
  count_files = {}
  
  for file in lst_files:
    str_file = Path(file)
    extension = str_file.suffix
    
    if extension:
      name_categories = search_categories(extension.lower())
      
      if name_categories not in count_files:
        count_files[name_categories] = {}
      
      if extension not in count_files[name_categories]:
        count_files[name_categories][extension] = 0
      count_files[name_categories][extension] += 1
  
  return count_files

def search_categories(extension: str) -> str:
  for key, value in FILE_CATEGORIES.items():
    if isinstance(value, list) and extension in value:
      return key
  return "Other"


def main():
  list_files = list_all_files()
  count_files_type = counting_files_type(list_files)
  if len(count_files_type) > 0:
    for key, value in count_files_type.items():
      print(key, value)
  else:
    print('Файлы не найдены.')

if __name__ == '__main__':
  main()