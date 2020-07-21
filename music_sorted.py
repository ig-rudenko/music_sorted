import os
import mutagen.flac
import mutagen.mp3
import mutagen
from re import findall
from sys import argv

path = input("Укажите директорию для сортировки: ")
music_list = os.listdir(path)
for track in music_list:
    print(track)
    # FLAC
    if str(findall(r".+\.(\S+)", track)) == "['flac']":
        tags_flac = mutagen.flac.FLAC(f"music\\{track}")        # Вытягиваем теги
        tags_flac_str = str(tags_flac.pprint()).split('\n')     # Преобразуем в список

        album_flac = str([line.split("=")[1] for line in tags_flac_str if "ALBUM=" in line])[2:-2]  # Переменная "Альбом"
        year_flac = str([line.split("=")[1] for line in tags_flac_str if "DATE=" in line])[2:-2]  # Переменная "Год (Альбома)"
        artist_flac = str([line.split("=")[1] for line in tags_flac_str if "ALBUMARTIST=" in line])[2:-2]  # Переменная "Артист"

        if not os.path.exists(f"{path}\\{artist_flac}\\[{year_flac}] {album_flac}"): # Если папка с альбомом НЕ создана, то...
            os.makedirs(f"{path}\\{artist_flac}\\[{year_flac}] {album_flac}")   # ...создаем
            print(f"Была создана папка: music\\{artist_flac}\\[{year_flac}] {album_flac}")
        os.replace(f"{path}\\{track}", f"{path}\\{artist_flac}\\[{year_flac}] {album_flac}\\{track}")  # Перемещаем файл
        print(f"Файл {track} был перемещен в папку {path}\\{artist_flac}\\[{year_flac}] {album_flac}")

    # MP3
    if str(findall(r".+\.(\S+)", track)) == "['mp3']":
        tag_mp3 = mutagen.File(f"music\\{track}")         # Вытягиваем теги
        tags_mp3 = str(tag_mp3.pprint()).split('\n')      # Преобразуем в список

        album_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TALB=" in line])[2:-2]     # Переменная "Альбом"
        year_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TDRC=" in line])[2:-2]      # Переменная "Год (Альбома)"
        artist_mp3 = str([line.split("=")[1] for line in tags_mp3 if "TPE1=" in line])[2:-2]    # Переменная "Артист"

        if not os.path.exists(f"{path}\\{artist_mp3}\\[{year_mp3}] {album_mp3}"): # Если папка с альбомом НЕ создана, то...
            os.makedirs(f"{path}\\{artist_mp3}\\[{year_mp3}] {album_mp3}")   # ...создаем
            print(f"Была создана папка: {path}\\{artist_mp3}\\[{year_mp3}] {album_mp3}")
        os.replace(f"{path}\\{track}", f"{path}\\{artist_mp3}\\[{year_mp3}] {album_mp3}\\{track}")  # Перемещаем файл
        print(f"Файл {track} был перемещен в папку {path}\\{artist_mp3}\\[{year_mp3}] {album_mp3}")

