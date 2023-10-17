import os
import shutil
from concurrent.futures import ThreadPoolExecutor

baza_for_filtr = {
    "images": ["JPG", "PNG", "JPEG"],
    "audio": ["MP3", "WAV", "WMA", "M4A"],
    "video": ["MP4", "MKV", "AVI", "MOV", "MPEG"],
    "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX", "XLS", "PPT", "ODT"],
    "archives": ["ZIP", "RAR", "TAR", "GZ", "7Z"]
}

MAX_THREADS = 10  # Кількість потоків

def create_folders_from_list(main_path, folder_list):
    for folder_name in folder_list:
        folder_path = os.path.join(main_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    return folder_list

def get_files_recursive(folder_path, excluz):
    all_files = []
    for foldername, subfolders, filenames in os.walk(folder_path):
        if os.path.basename(foldername) not in excluz:
            for filename in filenames:
                all_files.append(os.path.join(foldername, filename))
    return all_files

def move_files(file_path, main_path):
    file_extension = str(file_path).split('.')[-1].upper()
    for folder, extensions in baza_for_filtr.items():
        if file_extension in extensions:
            destination_folder = os.path.join(main_path, folder)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            destination = os.path.join(destination_folder, os.path.basename(file_path))
            if os.path.exists(file_path):
                try:
                    shutil.move(file_path, destination)
                except Exception as e:
                    print(f'\nПомилка при переміщенні файлу "{file_path}" до "{destination}". Помилка: {e}\n')

def remove_empty_folders(path):
    if not os.path.isdir(path):
        return
    for folder in os.listdir(path):
        full_path = os.path.join(path, folder)
        remove_empty_folders(full_path)
    folder_contents = os.listdir(path)
    if not folder_contents:
        os.rmdir(path)
        

def worker(file_path, main_path):
    move_files(file_path, main_path)

def get_sort(folder_path):
    excluz = create_folders_from_list(folder_path, list(baza_for_filtr.keys()))
    all_files = get_files_recursive(folder_path, excluz)
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for file_path in all_files:
            executor.submit(worker, file_path, folder_path)

    remove_empty_folders(folder_path)

if __name__ == "__main__":
    main_folder = input('\nEnter path: ')
    get_sort(main_folder)
    print(f'\nСортування завершено!\n')
