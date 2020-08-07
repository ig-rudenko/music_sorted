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
from tkinter import *
from tkinter import filedialog as fd

if os.name == "nt":     # Если ОС - Windows
    SL = "\\"
else:                   # Если ОС - Unix/Linux
    SL = "/"


def welcome():
    print("_________________Music Sorted_________________"
          "")


def delete_empty_folders(path):
    '''
    Удаляет рекурсивно все пустые папки
    :param path: Путь до папки, которую необходимо удалить, если она пустая
    :return: ничего
    '''
    dir_list = os.listdir(path)                                 # Смотрим все объекты в папке
    if dir_list:                                                # Если папка не пуста, то...
        for element in dir_list:                                    # ...проверяем каждый объект
            if os.path.isdir(f"{path}{SL}{element}"):                   # Если это папка, то...
                delete_empty_folders(f"{path}{SL}{element}")                # ...рекурсия.
    try:
        os.rmdir(path)                                          # ...пробуем удалить текущую папку
        print(f"Папка {path} удалена!")
    except Exception as e:
        print(f"Ошибка при удалении папки: {e}")


# ---------------------------------------------СОРТИРОВКА "СБОРНИК"-----------------------------------------------------


def list_dir(path):
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
            remove_files_from_dir(path, True, album_name)    # Данная папка это "Альбом"

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
    # try:
    #     os.rmdir(path)
    # except Exception:
    #     print(f"В папке {path} остались файлы")


# ---------------------------------------------НЕЗАВИСИМАЯ СОРТИРОВКА---------------------------------------------------


def sorted_each_file(path, tab=4):
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
                tags_flac = mutagen.flac.FLAC(f"{path}{SL}{track}")        # Вытягиваем теги
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
                tag_mp3 = mutagen.File(f"{path}{SL}{track}")         # Вытягиваем теги
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


# -----------------------------------------------------СТАРТ------------------------------------------------------------


def menu_1():
    menu = Menu(window)
    new_item = Menu(menu, tearoff=0)
    new_item.add_command(label='Новый')
    new_item.add_separator()
    new_item.add_command(label='Изменить')
    menu.add_cascade(label='Файл', menu=new_item)
    window.config(menu=menu)
    window.mainloop()


def open_folder():
    file_name = fd.askopenfilename()
    


if __name__ == "__main__":
    # welcome()
    # ROOT_DIR = input("Введите полный путь до папки: ")
    # sort_type = input("Выполнить сортировку как для 'сборников'? [y/n]: ").upper()
    # check_folder_delete = input("Удалить пустые папки после перемещения? [Y/n]").upper()
    # # if sort_type == 'Y':
    # print("\n", "_"*10, "Выполняем сортировку типа 'Сборник'", "_"*10)
    # #     list_dir(ROOT_DIR)
    # # else:
    # print("\n", "_" * 10, "Выполняем независимую сортировку", "_" * 10)
    # #     sorted_each_file(ROOT_DIR)
    # if check_folder_delete == 'Y' or check_folder_delete == '':
    #     print("\n", "_"*10, "Удаляем пустые папки", "_"*10)
    #     delete_empty_folders(ROOT_DIR)
    # input("\nНажмите Enter, чтобы выйти...")

    window = Tk()
    window.title("Добро пожаловать в приложение PythonRu")
    window.geometry('400x250')
    menu = Menu(window)
    new_item = Menu(menu, tearoff=0)
    new_item.add_command(label='Новый', command=menu_1)
    new_item.add_separator()
    menu.add_cascade(label='Файл', menu=new_item)
    window.config(menu=menu)
    window.mainloop()

