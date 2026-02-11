from pathlib import Path

def create_def_conf(config_path):
  default_content = f"""
# Какие папки сортировать
"watch_folder": {str(Path.cwd())}

# Режим предпросмотра: true = только смотрим, false = реально перемещаем
"dry_run": true

# Куда складывать отсортированное
"output_base": {str(Path.cwd())}
  """
  
  with open(config_path, 'w', encoding="utf-8") as f:
    f.write(default_content)