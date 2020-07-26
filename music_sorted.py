import os
import mutagen.flac
import mutagen.mp3
import mutagen
from re import findall
from sys import argv

ROOT_DIR = input("Укажите директорию для сортировки: ")

if os.name == "nt":     # Если ОС - Windows
    SL = "\\"
else:                   # Если ОС - Unix/Linux
    SL = "/"


def music_sorted(path=ROOT_DIR, tab=4):
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

                year, artist, album = replace_file(path, track, artist, year, album, 2*tab)

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

                year, artist, album = replace_file(path, track, artist, year, album, 2*tab)

            if os.path.isdir(f"{path}{SL}{track}"):                     # Если это папка, то...
                print("-"*(tab-4)+f"DIR: {track}")
                music_sorted(path=f"{path}{SL}{track}", tab=tab+4)          # ...рекурсия

        except Exception as e:
            print(" "*tab+str(e))


def replace_file(path, track, artist, year, album, tab):
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


music_sorted()
input("Нажмите Enter для выхода.")

