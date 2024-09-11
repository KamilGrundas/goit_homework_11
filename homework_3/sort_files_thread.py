import os
import shutil
from threading import Thread

sort_threads = []
move_threads = []

IMAGE_EXT = (".jpeg", ".png", ".jpg", ".svg", ".bmp")
VIDEO_EXT = (".avi", ".mp4", ".mov", ".mkv")
DOCUMENT_EXT = (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx")
MUSIC_EXT = (".mp3", ".ogg", ".wav", ".amr")
ARCHIVE_EXT = (".zip", ".gz", ".tar", ".rar")

def check_ext(ext):

    if ext in IMAGE_EXT:
        category = "images"

    elif ext in VIDEO_EXT:
        category = "video"

    elif ext in DOCUMENT_EXT:
        category = "documents"

    elif ext in MUSIC_EXT:
        category = "music"

    elif ext in ARCHIVE_EXT:
        category = "archives"

    else:
        category = "other"

    target_dir = os.path.join(path, category)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    return target_dir

def normalize(text):
    normalization_dict = {
        "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
        "ó": "o", "ś": "s", "ż": "z", "ź": "z"
    }
    
    normalized_text = "".join(normalization_dict.get(char, char) for char in text)
    return "".join(char if char.isalnum() or char.isspace() else "_" for char in normalized_text)

def move_files(new_file_name, file_ext ,file_path, target_dir):

    file_name_length = len(new_file_name)
    target_path = os.path.join(target_dir, (new_file_name + file_ext))
    count = 0

    if not target_path == file_path:

        while os.path.exists(target_path):
            count += 1
            new_file_name = new_file_name[0:file_name_length] + "_" + str(count)
            target_path = os.path.join(target_dir, (new_file_name + file_ext))
        shutil.move(file_path, target_path)


def sort_folder(root, files):
    for file in files:
        dot_position = file.rfind(".")
        file_name = file[0:dot_position]
        file_ext = file[dot_position:]
        target_dir = check_ext(file_ext)
        file_path = os.path.join(root, file)


        new_file_name = normalize(file_name)
        move_thread = Thread(target = move_files, args = (new_file_name, file_ext, file_path, target_dir))
        move_threads.append(move_thread)
        move_thread.start()

    for move_thread in move_threads:
        move_thread.join()


def sort_files(path):

    for root, dirs, files in os.walk(path):
        sort_thread = Thread(target = sort_folder, args = (root, files))
        sort_threads.append(sort_thread)
        sort_thread.start()

    for sort_thread in sort_threads:
        sort_thread.join()

    for root, dirs, files in os.walk(path, topdown=False): # removes empty directories
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
    print("Success")

path = input("Input path to directory you want to sort e.g: C:/Users/john/Desktop/all_files\nPath: ")

sort_files(path)