# -*- coding: utf-8 -*-

'''
    Для создания .exe файла была использована следующая команда:
        pyinstaller --onedir --onefile --name=Music_Sorted MS.py
'''

import os
import mutagen.flac
import mutagen.mp3
import mutagen
from re import findall

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
            print(f"     {element}")
            tags_flac = mutagen.flac.FLAC(f"{path}{SL}{element}")   # Вытягиваем теги
            tags_flac_str = str(tags_flac.pprint()).split('\n')     # Преобразуем в список

            album_flac = str([line.split("=")[1] for line in tags_flac_str
                              if "album" in line.lower() and "artist" not in line.lower()])[2:-2]  # Переменная "Альбом"
            album_flac = album_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*"," ").replace(
                "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()

            if not album_name:                                 # Если переменная для проверки альбомов не создана, то...
                album_name = album_flac                            # ...создаем
            else:
                if album_name.upper() != album_flac.upper():   # Если "Альбомы" различаются, то...
                    print("~COMPILATION~")
                    remove_files_from_dir(path, False)             # ...это компиляция
                    break                                          # выход из цикла.

        if str(findall(r".+\.(\S+)", element)) == "['mp3']":
            print(f"     {element}")
            tag_mp3 = mutagen.File(f"{path}{SL}{element}")     # Вытягиваем теги
            tags_mp3 = str(tag_mp3.pprint()).split('\n')       # Преобразуем в список

            album_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TALB" in line.upper()])[2:-2]  # Переменная "Альбом"
            album_mp3 = album_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()

            if not album_name:                                 # Если переменная для проверки альбомов не создана, то...
                album_name = album_mp3                             # ...создаем
            else:
                if album_name.upper() != album_mp3.upper():    # Если "Альбомы" различаются, то...
                    print("~COMPILATION~")
                    remove_files_from_dir(path, False)             # ...это компиляция
                    break                                          # выход из цикла.

    else:
        if album_name:
            print(f"~ALBUM~\n{album_name}\n")
            remove_files_from_dir(path, True, album_name=album_name)    # Данная папка это "Альбом"

    for dir_ in dir_list:
        if os.path.isdir(f"{path}{SL}{dir_}"):                     # Если это папка, то...
            print(f"\nDIR: {dir_}")
            list_dir(path=f"{path}{SL}{dir_}")                         # ...рекурсия


def remove_files_from_dir(path, is_album, album_name=''):
    '''
    Перемещает все файлы из директории 'path' в зависимости от 'is_album'
    :param path: полный путь до директории
    :param is_album: Альбом: 'True' или Компиляция: 'False'
    :param album_name: Название альбома, по умолчанию пустая строка ''
    :return:
    '''

    # АЛЬБОМ
    if is_album:
        music_list = os.listdir(path)
        year = ''
        artist = ''
        for track in music_list:
            if not year or not artist:          # Если тег год альбома или артист еще не найден, то...
                try:                                # ...пытаемся найти
                    # FLAC
                    if str(findall(r".+\.(\S+)", track)) == "['flac']":
                        tags_flac = mutagen.flac.FLAC(f"{path}{SL}{track}")  # Вытягиваем теги
                        tags_flac_str = str(tags_flac.pprint()).split('\n')  # Преобразуем в список

                        year_flac = str([line.split("=")[1] for line in tags_flac_str
                                         if "date=" in line.lower() and "orig" not in line.lower()])[2:-2]  # Переменная "Год (Альбома)"
                        year = year_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                            "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()
                        artist_flac = str([line.split("=")[1] for line in tags_flac_str
                                           if "artist" in line.lower() and "album" not in line.lower()])[2:-2]  # Переменная "Артист"
                        artist = artist_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace(
                            "*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()

                    # MP3
                    elif str(findall(r".+\.(\S+)", track)) == "['mp3']":
                        tag_mp3 = mutagen.File(f"{path}{SL}{track}")  # Вытягиваем теги
                        tags_mp3 = str(tag_mp3.pprint()).split('\n')  # Преобразуем в список
                        year_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TDRC" in line.upper()])[2:-2]  # Переменная "Год (Альбома)"
                        year = year_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                            "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()
                        artist_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TPE1" in line.upper()])[2:-2]  # Переменная "Артист"
                        artist = artist_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace(
                            "*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()

                except Exception as e:
                    print(e)
            # Когда нашли все необходимые теги, то прерываем цикл
            else:
                break

        # Если теги не найдены, то это компиляция
        else:
            try:
                if not os.path.exists(f"{ROOT_DIR}{SL}Compilations"):  # Если нет папки "Compilations", то...
                    os.makedirs(f"{ROOT_DIR}{SL}Compilations")  # ...создаем
                *_, curr_dir = str(path).split(SL)  # Вытягиваем название папки с музыкой
                os.replace(path, f'{ROOT_DIR}{SL}Compilations{SL}{curr_dir}')  # Перемещаем папку с музыкой в Compilations
                print(f"Была создана компиляция {curr_dir} в папке {ROOT_DIR}{SL}Compilations")
                return 0
            except Exception as e:
                print(e)

        # Перемещаем все файлы в папку альбома
        try:
            end_dir = f"{ROOT_DIR}{SL}Artist_Album{SL}{artist}{SL}[{year}] {album_name}"
            if not os.path.exists(end_dir):                                 # Если папка с альбомом НЕ создана, то...
                os.makedirs(end_dir)                                            # ...создаем
                print(f"Была создана папка: {end_dir}")
            for file in music_list:
                os.replace(f"{path}{SL}{file}", f"{end_dir}{SL}{file}")     # Перемещаем файл
                print(f"    Файл \"{file}\" был перемещен в папку {end_dir}")
            else:
                print(f"АЛЬБОМ: \"[{year}] {album_name}\" был успешно собран!")
        except Exception as e:
            print(e)

    # КОМПИЛЯЦИЯ
    else:
        try:
            if not os.path.exists(f"{ROOT_DIR}{SL}Compilations"):               # Если нет папки "Compilations", то...
                os.makedirs(f"{ROOT_DIR}{SL}Compilations")                          # ...создаем
            *_, curr_dir = str(path).split(SL)                                  # Вытягиваем название папки с музыкой
            os.replace(path, f'{ROOT_DIR}{SL}Compilations{SL}{curr_dir}')       # Перемещаем папку с музыкой в Compilations
            print(f"Была создана компиляция: \"{curr_dir}\" в папке {ROOT_DIR}{SL}Compilations")
            return 0
        except Exception as e:
            print(e)

    # Удаляем пустую папку
    try:
        os.rmdir(path)
    except Exception:
        print(f"В папке {path} остались файлы")


def sorted_each_file(path=ROOT_DIR, tab=4):
    '''
    Функция перебирает все файлы .flac и .mp3 в папке, которая ей передана и
    в зависимости от тегов перемещает в нужные папки

    :param path:    полный путь до папки
    :param tab:     количество отступов
    :return:        ничего
    '''
    year = ''
    artist = ''
    album = ''
    music_list = os.listdir(path)
    for track in music_list:
        print(" "*tab+f" {track}")
        try:
            # FLAC
            if str(findall(r".+\.(\S+)", track)) == "['flac']":
                tags_flac = mutagen.flac.FLAC(f"{path}\{track}")        # Вытягиваем теги
                tags_flac_str = str(tags_flac.pprint()).split('\n')     # Преобразуем в список

                album_flac = str([line.split("=")[1] for line in tags_flac_str
                                  if "album" in line.lower() and "artist" not in line.lower()])[2:-2]  # Переменная "Альбом"
                album = album_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                    "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()
                year_flac = str([line.split("=")[1] for line in tags_flac_str
                                 if "date=" in line.lower() and "orig" not in line.lower()])[2:-2]  # Переменная "Год (Альбома)"
                year = year_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                    "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()
                artist_flac = str([line.split("=")[1] for line in tags_flac_str
                                   if "artist" in line.lower() and "album" not in line.lower()])[2:-2]  # Переменная "Артист"
                artist = artist_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace(
                    "*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()

                year, artist, album = replace_file_by_tags(path, track, artist, year, album, 2 * tab)

            # MP3
            if str(findall(r".+\.(\S+)", track)) == "['mp3']":
                tag_mp3 = mutagen.File(f"{path}\{track}")         # Вытягиваем теги
                tags_mp3 = str(tag_mp3.pprint()).split('\n')      # Преобразуем в список

                album_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TALB" in line.upper()])[2:-2]  # Переменная "Альбом"
                album = album_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                    "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()
                year_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TDRC" in line.upper()])[2:-2]  # Переменная "Год (Альбома)"
                year = year_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(
                    "?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()
                artist_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TPE1" in line.upper()])[2:-2]  # Переменная "Артист"
                artist = artist_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace(
                    "*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").strip()

                year, artist, album = replace_file_by_tags(path, track, artist, year, album, 2 * tab)

            if os.path.isdir(f"{path}{SL}{track}"):                     # Если это папка, то...
                print("-"*(tab-4)+f"DIR: {track}")
                sorted_each_file(path=f"{path}{SL}{track}", tab=tab+4)          # ...рекурсия

        except Exception as e:
            print(" "*tab+str(e))


def replace_file_by_tags(path, track, artist, year, album, tab):
    '''
    Функция анализирует теги и перемещает файлы в соответствующие папки

    :param path:    полный путь до папки с файлами
    :param track:   название файла в папке
    :param artist:  тег с именем артиста
    :param year:    тег с годом выпуска альбома
    :param album:   тег с названием альбома
    :param tab:     регулирует количество отступов
    :return:        функция возвращает пустые теги '', '', ''
    '''
    # Если все необходимые теги найдены
    if year and artist and album:
        end_dir = f"{ROOT_DIR}{SL}Artists{SL}{artist}{SL}[{year}] {album}"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    # Если нет только года выпуска альбома
    elif artist and album and not year:
        end_dir = f"{ROOT_DIR}{SL}Artists{SL}{artist}{SL}{album}"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    # Если есть только артист
    elif artist and not album:
        end_dir = f"{ROOT_DIR}{SL}Artists{SL}{artist}"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    # Если тегов нет, то помещаем в папку "Unknowns"
    else:
        end_dir = f"{ROOT_DIR}{SL}Unknowns"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    return '', '', ''


sort_type = input("Выполнить сортировку как для 'сборников'? [Y/N]: ").upper()
if sort_type == 'Y':
    list_dir()
else:
    sorted_each_file()
input("\nНажмите Enter, чтобы выйти...")
