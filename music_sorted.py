import os
import mutagen.flac
import mutagen.mp3
import mutagen
from re import findall
from sys import argv

path = input("Укажите директорию для сортировки: ")
music_list = os.listdir(path)
for track in music_list:
    try:
        print(track)
        # FLAC
        if str(findall(r".+\.(\S+)", track)) == "['flac']":
            tags_flac = mutagen.flac.FLAC(f"{path}\{track}")        # Вытягиваем теги
            tags_flac_str = str(tags_flac.pprint()).split('\n')     # Преобразуем в список
            print(tags_flac_str)
            album_flac = str([line.split("=")[1] for line in tags_flac_str if "album=" in line.lower()])[2:-2]  # Переменная "Альбом"
            album_flac = album_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
            year_flac = str([line.split("=")[1] for line in tags_flac_str if "date=" in line.lower()])[2:-2]  # Переменная "Год (Альбома)"
            year_flac = year_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
            artist_flac = str([line.split("=")[1] for line in tags_flac_str if "albumartist=" in line.lower()])[2:-2]  # Переменная "Артист"
            artist_flac = artist_flac.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
            print(artist_flac, year_flac, album_flac)

            if not os.path.exists(f"{path}\{artist_flac}\[{year_flac}] {album_flac}"): # Если папка с альбомом НЕ создана, то...
                os.makedirs(f"{path}\{artist_flac}\[{year_flac}] {album_flac}")   # ...создаем
                print(f"Была создана папка: {path}\{artist_flac}\[{year_flac}] {album_flac}")
            os.replace(f"{path}\\{track}", f"{path}\{artist_flac}\[{year_flac}] {album_flac}\{track}")  # Перемещаем файл
            print(f"Файл {track} был перемещен в папку {path}\{artist_flac}\[{year_flac}] {album_flac}")

        # MP3
        if str(findall(r".+\.(\S+)", track)) == "['mp3']":
            tag_mp3 = mutagen.File(f"{path}\{track}")         # Вытягиваем теги
            tags_mp3 = str(tag_mp3.pprint()).split('\n')      # Преобразуем в список

            album_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TALB=" in line.upper()])[2:-2]     # Переменная "Альбом"
            album_mp3 = album_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
            year_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TDRC=" in line.upper()])[2:-2]      # Переменная "Год (Альбома)"
            year_mp3 = year_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
            artist_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TPE1=" in line.upper()])[2:-2]    # Переменная "Артист"
            artist_mp3 = artist_mp3.replace(":", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")

            if not os.path.exists(f"{path}\{artist_mp3}\[{year_mp3}] {album_mp3}"): # Если папка с альбомом НЕ создана, то...
                os.makedirs(f"{path}\{artist_mp3}\[{year_mp3}] {album_mp3}")   # ...создаем
                print(f"Была создана папка: {path}\{artist_mp3}\[{year_mp3}] {album_mp3}")
            os.replace(f"{path}\{track}", f"{path}\{artist_mp3}\[{year_mp3}] {album_mp3}\{track}")  # Перемещаем файл
            print(f"Файл {track} был перемещен в папку {path}\{artist_mp3}\[{year_mp3}] {album_mp3}")
    except Exception as e:
        print(e)

input("Нажмите Enter для выхода.")

