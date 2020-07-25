# -*- coding: utf-8 -*-
import os
import mutagen.flac
import mutagen.mp3
import mutagen
from re import findall
from sys import argv

# ROOT_DIR = "C:\\Users\\Igor\\PycharmProjects\\music_sorted\\music"
ROOT_DIR = input("Введите полный путь до папки: ")

if os.name == "nt":     # Если ОС - Windows
    SL = "\\"
else:                   # Если ОС - Unix/Linux
    SL = "/"


def list_dir(path=ROOT_DIR):
    '''
    Проверяет, является ли текущая директория промежуточной или конечной (альбомом)
    Если так, то определяет тип: альбом или компиляция
    :param path: полный путь до директории
    :return:
    '''
    dir_list = os.listdir(path)
    album_name = ''

    for element in dir_list:

        if str(findall(r".+\.(\S+)", element)) == "['flac']":
            print(element)
            tags_flac = mutagen.flac.FLAC(f"{path}{SL}{element}")   # Вытягиваем теги
            tags_flac_str = str(tags_flac.pprint()).split('\n')     # Преобразуем в список

            album_flac = str([line.split("=")[1] for line in tags_flac_str if "album=" in line.lower()])[
                         2:-2]  # Переменная "Альбом"
            album_flac = album_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*",
                                                                                                   " ").replace("?",
                                                                                                                " ").replace(
                "\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")

            if not album_name:                                 # Если переменная для проверки альбомов не создана, то...
                album_name = album_flac                            # ...создаем
            else:
                if album_name.upper() != album_flac.upper():   # Если "Альбомы" различаются, то...
                    remove_files_from_dir(path, False)             # ...это компиляция
                    print("COMPILATION")
                    break                                          # выход из цикла.

        if str(findall(r".+\.(\S+)", element)) == "['mp3']":
            print(element)
            tag_mp3 = mutagen.File(f"{path}{SL}{element}")     # Вытягиваем теги
            tags_mp3 = str(tag_mp3.pprint()).split('\n')       # Преобразуем в список

            album_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TALB=" in line.upper()])[
                        2:-2]  # Переменная "Альбом"
            album_mp3 = album_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")

            if not album_name:                                 # Если переменная для проверки альбомов не создана, то...
                album_name = album_mp3                             # ...создаем
            else:
                if album_name.upper() != album_mp3.upper():    # Если "Альбомы" различаются, то...
                    remove_files_from_dir(path, False)             # ...это компиляция
                    print("COMPILATION")
                    break                                          # выход из цикла.

    else:
        if album_name:
            print("ALBUM!")
            remove_files_from_dir(path, True, album_name=album_name)    # Данная папка это "Альбом"

    for dir_ in dir_list:
        if os.path.isdir(f"{path}{SL}{dir_}"):                     # Если это папка, то...
            print(f"DIR: {dir_}")
            list_dir(path=f"{path}{SL}{dir_}")                         # ...рекурсия


def remove_files_from_dir(path, is_album, album_name=''):
    '''
    Перемещает все файлы из директории 'path' в зависимости от 'is_album'
    :param path: полный путь до директории
    :param is_album: Альбом: 'True' или Компиляция: 'False'
    :param album_name: Название альбома, по умолчанию пустая строка ''
    :return:
    '''

    if is_album:                                # Если это альбом
        music_list = os.listdir(path)
        other_files = []
        for track in music_list:
            try:
                # FLAC
                if str(findall(r".+\.(\S+)", track)) == "['flac']":
                    tags_flac = mutagen.flac.FLAC(f"{path}{SL}{track}")  # Вытягиваем теги
                    tags_flac_str = str(tags_flac.pprint()).split('\n')  # Преобразуем в список
                    year_flac = str([line.split("=")[1] for line in tags_flac_str if "date=" in line.lower()])[
                                2:-2]  # Переменная "Год (Альбома)"
                    year = year_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                        "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
                    artist_flac = str([line.split("=")[1] for line in tags_flac_str if "albumartist=" in line.lower()])[
                                  2:-2]  # Переменная "Артист"
                    artist = artist_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*",
                                                                                                             " ").replace(
                        "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")

                    end_dir = f'{ROOT_DIR}{SL}Artist_Album{SL}{artist}{SL}[{year}] {album_name}'
                    if not os.path.exists(end_dir):                    # Если папка с альбомом НЕ создана, то...
                        os.makedirs(end_dir)                               # ...создаем
                        print(f"Была создана папка: {end_dir}")
                    os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
                    print(f"Файл {track} был перемещен в папку {end_dir}")

                # MP3
                elif str(findall(r".+\.(\S+)", track)) == "['mp3']":
                    tag_mp3 = mutagen.File(f"{path}{SL}{track}")  # Вытягиваем теги
                    tags_mp3 = str(tag_mp3.pprint()).split('\n')  # Преобразуем в список
                    year_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TDRC=" in line.upper()])[
                               2:-2]  # Переменная "Год (Альбома)"
                    year = year_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                        "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
                    artist_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TPE1=" in line.upper()])[
                                 2:-2]  # Переменная "Артист"
                    artist = artist_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*",
                                                                                                           " ").replace("?",
                                                                                                                        " ").replace(
                        "\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")

                    end_dir = f"{ROOT_DIR}{SL}Artist_Album{SL}{artist}{SL}[{year}] {album_name}"
                    if not os.path.exists(end_dir):                     # Если папка с альбомом НЕ создана, то...
                        os.makedirs(end_dir)                                   # ...создаем
                        print(f"Была создана папка: {end_dir}")
                    os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
                    print(f"Файл {track} был перемещен в папку {end_dir}")

                # OTHER FILES
                else:
                    if not other_files:
                        other_files = [track.strip()]
                    else:
                        other_files.append(track.strip())

            except Exception as e:
                print(e)

        # Перенос папок и не музыкальных файлов
        if other_files:
            for file in other_files:
                try:
                    if not os.path.exists(end_dir):                          # Если папка с альбомом НЕ создана, то...
                        os.makedirs(end_dir)                                     # ...создаем
                        print(f"Была создана папка: {end_dir}")
                    os.replace(f"{path}{SL}{file}", f"{end_dir}{SL}{file}")  # Перемещаем
                    if os.path.isdir(f"{path}{SL}{file}"):
                        print(f"Папка {file} была перемещена в папку {end_dir}")
                    else:
                        print(f"Файл {file} был перемещен в папку {end_dir}")

                except Exception as e:
                    print(e)
            else:
                os.rmdir(path)


    else:
        if not os.path.exists(f"{ROOT_DIR}{SL}Compilations"):               # Если нет папки "Compilations", то...
            os.makedirs(f"{ROOT_DIR}{SL}Compilations")                          # ...создаем
        *_, curr_dir = str(path).split(SL)                                  # Вытягиваем название папки с музыкой
        os.replace(path, f'{ROOT_DIR}{SL}Compilations{SL}{curr_dir}')       # Перемещаем папку с музыкой в Compilations
        print(f"Была создана компиляция {curr_dir} в папке {ROOT_DIR}{SL}Compilations")


list_dir()

