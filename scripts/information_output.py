import main

LIST_ALL_FILES = main.list_all_files()
COUNT_FILES_TYPE = main.counting_files_type(LIST_ALL_FILES)



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