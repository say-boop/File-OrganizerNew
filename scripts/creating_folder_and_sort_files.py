from pathlib import Path
import shutil
import main

folder_name = 'folder'
path = main.find_folder_path()
result_path = path / folder_name 

result_path.mkdir(parents=True, exist_ok=True)
print('Папка создана')

list_files = [child.name for child in path.iterdir() if child.is_file()]

print('Сортировка начата')

for file in list_files:
  source = path / file
  shutil.move(source, result_path)

print('Сортировка завершена')