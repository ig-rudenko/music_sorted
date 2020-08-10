# -*- coding: utf-8 -*-

'''
    Для создания .exe файла была использована следующая команда:
        pyinstaller --onedir --onefile --icon="music_sorted_icon.ico" --noconsole --name=Music_Sorted_gui MS_gui.py
'''

import os
import mutagen.flac
import mutagen.mp3
import mutagen
from re import findall
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

if os.name == "nt":     # Если ОС - Windows
    SL = "\\"
else:                   # Если ОС - Unix/Linux
    SL = "/"


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


def list_dir(root_dir, path):
    '''
    Проверяет, является ли текущая директория промежуточной или конечной (альбомом)
    Если так, то определяет тип: альбом или компиляция
    :param root_dir:    Корневая директория
    :param path:        Полный путь до директории
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
                    remove_files_from_dir(root_dir, path, False)             # ...это компиляция
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
                    remove_files_from_dir(root_dir, path, False)             # ...это компиляция
                    break                                          # выход из цикла.

    else:
        if album_name:
            print(f"~ALBUM~\n{album_name}\n")
            remove_files_from_dir(root_dir, path, True, album_name)    # Данная папка это "Альбом"

    for dir_ in dir_list:
        if os.path.isdir(f"{path}{SL}{dir_}"):                     # Если это папка, то...
            print(f"\nDIR: {dir_}")
            list_dir(root_dir, path=f"{path}{SL}{dir_}")                         # ...рекурсия


def remove_files_from_dir(root_dir, path, is_album, album_name=''):
    '''
    Перемещает все файлы из директории 'path' в зависимости от 'is_album'
    :param root_dir:    Корневая директория
    :param path:        Полный путь до директории
    :param is_album:    Альбом: 'True' или Компиляция: 'False'
    :param album_name:  Название альбома, по умолчанию пустая строка ''
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
                if not os.path.exists(f"{root_dir}{SL}Compilations"):  # Если нет папки "Compilations", то...
                    os.makedirs(f"{root_dir}{SL}Compilations")  # ...создаем
                *_, curr_dir = str(path).split(SL)  # Вытягиваем название папки с музыкой
                os.replace(path, f'{root_dir}{SL}Compilations{SL}{curr_dir}')  # Перемещаем папку с музыкой в Compilations
                print(f"Была создана компиляция {curr_dir} в папке {root_dir}{SL}Compilations")
                return 0
            except Exception as e:
                print(e)

        # Перемещаем все файлы в папку альбома
        try:
            end_dir = f"{root_dir}{SL}Artist_Album{SL}{artist}{SL}[{year}] {album_name}"
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
            if not os.path.exists(f"{root_dir}{SL}Compilations"):               # Если нет папки "Compilations", то...
                os.makedirs(f"{root_dir}{SL}Compilations")                          # ...создаем
            *_, curr_dir = str(path).split(SL)                                  # Вытягиваем название папки с музыкой
            os.replace(path, f'{root_dir}{SL}Compilations{SL}{curr_dir}')       # Перемещаем папку с музыкой в Compilations
            print(f"Была создана компиляция: \"{curr_dir}\" в папке {root_dir}{SL}Compilations")
            return 0
        except Exception as e:
            print(e)


# ---------------------------------------------НЕЗАВИСИМАЯ СОРТИРОВКА---------------------------------------------------


def sorted_each_file(root_dir, path, tab=4):
    '''
    Функция перебирает все файлы .flac и .mp3 в папке, которая ей передана и
    в зависимости от тегов перемещает в нужные папки
    :param root_dir:    Корневая директория
    :param path:        Полный путь до папки
    :param tab:         Количество отступов
    :return:            Ничего
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

                year, artist, album = replace_file_by_tags(root_dir, path, track, artist, year, album, 2 * tab)

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

                year, artist, album = replace_file_by_tags(root_dir, path, track, artist, year, album, 2 * tab)

            if os.path.isdir(f"{path}{SL}{track}"):                     # Если это папка, то...
                print("-"*(tab-4)+f"DIR: {track}")
                sorted_each_file(root_dir, path=f"{path}{SL}{track}", tab=tab + 4)          # ...рекурсия

        except Exception as e:
            print(" "*tab+str(e))


def replace_file_by_tags(root_dir, path, track, artist, year, album, tab):
    '''
    Функция анализирует теги и перемещает файлы в соответствующие папки
    :param root_dir:    Корневая директория
    :param path:        Полный путь до папки с файлами
    :param track:       Название файла в папке
    :param artist:      Тег с именем артиста
    :param year:        Тег с годом выпуска альбома
    :param album:       Тег с названием альбома
    :param tab:         Регулирует количество отступов
    :return:            Функция возвращает пустые теги '', '', ''
    '''
    # Если все необходимые теги найдены
    if year and artist and album:
        end_dir = f"{root_dir}{SL}Artists{SL}{artist}{SL}[{year}] {album}"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    # Если нет только года выпуска альбома
    elif artist and album and not year:
        end_dir = f"{root_dir}{SL}Artists{SL}{artist}{SL}{album}"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    # Если есть только артист
    elif artist and not album:
        end_dir = f"{root_dir}{SL}Artists{SL}{artist}"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    # Если тегов нет, то помещаем в папку "Unknowns"
    else:
        end_dir = f"{root_dir}{SL}Unknowns"
        if not os.path.exists(end_dir):  # Если папка с альбомом НЕ создана, то...
            os.makedirs(end_dir)  # ...создаем
            print(" "*tab+f"Была создана папка: {end_dir}")
        os.replace(f"{path}{SL}{track}", f"{end_dir}{SL}{track}")  # Перемещаем файл
        print(" "*tab+f"Файл \"{track}\" был перемещен в папку {end_dir}")

    return '', '', ''


# ----------------------------------------------------- GUI ------------------------------------------------------------

row = 1
directories_in, directories_out = [], []
directory_in = ''


class Directory(object):
    def __init__(self):
        self.label_in_dir = Label(tab1, text=directory_in)
        self.label_in_dir.grid(column=0, row=row, sticky=W)

        self.button_del_line = Button(tab1,
                                      text=" X ",
                                      activeforeground='red',
                                      relief="groove",
                                      bd=1,
                                      command=self.delete)
        self.button_del_line.grid(column=1, row=row, sticky=W)

        self.button_set_out_dir = Button(tab1,
                                         text=" ▷ ",
                                         relief="groove",
                                         bd=1,
                                         command=self.result_dir)
        self.button_set_out_dir.grid(column=2, row=row, sticky=W)

        self.label_out_dir = Label(tab1, text='')
        self.button_same_out_dir_for_all = Button(tab1,
                                                  text="",
                                                  relief="groove",
                                                  bd=1,
                                                  command=self.same_out_dir_for_all)
        self.combo_sort_type = ttk.Combobox(tab1, values=("Сборник", "Независимая"))
        self.combo_sort_type.grid(column=5, row=row, sticky=W)
        self.combo_sort_type.current(0)
        self.redraw()

    def table_head(self):
        Label(tab1, text="    Директория сортировки    ").grid(column=0, row=0, sticky=N)
        Label(tab1, text="    Директория сохранения    ").grid(column=3, row=0, sticky=N)
        Label(tab1, text="    Применить для всех    ").grid(column=4, row=0, sticky=N)
        Label(tab1, text="    Тип сортировки    ").grid(column=5, row=0, sticky=N)

    def delete(self):
        global directories_in
        self.button_del_line.destroy()
        self.button_set_out_dir.destroy()
        self.label_in_dir.destroy()
        self.label_out_dir.destroy()
        self.button_same_out_dir_for_all.destroy()
        self.combo_sort_type.destroy()
        for position, elem in enumerate(directories_in):        # Проходимся по списку
            if elem == self:                                        # Если нашли текущий елемент, то...
                directories_in.pop(position)                            # ...удаляем по индексу
        self.redraw()                                           # Перерисовываем список объектов

    def redraw(self):
        global directories_in, row
        for position, elem in enumerate(directories_in, 1):
            elem.button_set_out_dir.grid(column=2, row=position, sticky=W)
            elem.button_del_line.grid(column=1, row=position, sticky=W)
            elem.label_in_dir.grid(column=0, row=position, sticky=W)
            elem.label_out_dir.grid(column=3, row=position, sticky=W)
            elem.combo_sort_type.grid(column=5, row=position, sticky=W)

            if elem.label_out_dir["text"]:
                if len(directories_in) == 1:
                    elem.button_same_out_dir_for_all.grid_remove()
                elif position == 1:
                    elem.button_same_out_dir_for_all["text"] = " ↓ "
                    elem.button_same_out_dir_for_all.grid(column=4, row=position, sticky=W)
                elif position == len(directories_in):
                    elem.button_same_out_dir_for_all["text"] = " ↑ "
                    elem.button_same_out_dir_for_all.grid(column=4, row=position, sticky=W)
                else:
                    elem.button_same_out_dir_for_all["text"] = " ↕ "
                    elem.button_same_out_dir_for_all.grid(column=4, row=position, sticky=W)
            else:
                elem.button_same_out_dir_for_all.grid_remove()

        row = len(directories_in) + 1

    def result_dir(self):
        global directories_out
        directory_out = filedialog.askdirectory()                   # Открываем диалоговое окно
        if directory_out:                                           # Если папка была выбрана, то...
            if self.label_out_dir["text"]:                              # Если уже существовал путь, то...
                self.label_out_dir.destroy()                                # ...обнуляем
            directories_out.append(directory_out)                       # ...добавляем в список
            self.label_out_dir = Label(tab1, text=directory_out)
            self.label_out_dir.grid(column=3, row=self.button_del_line.grid_info().get("row"), sticky=W)
            self.redraw()

    def same_out_dir_for_all(self):
        global directories_in
        for elem in directories_in:
            elem.label_out_dir["text"] = self.label_out_dir["text"]
        self.redraw()


def open_folder():
    global row, directories_in, directory_in
    directory_in = filedialog.askdirectory()                # Открываем диалоговое окно
    if directory_in:                                        # Если папка была выбрана, то...
        for item in directories_in:                         # ...листаем уже выбранные директории
            if directory_in == item.label_in_dir["text"]:       # Если такая директория уже добавлена, то...
                break                                               # ...пропуск
        else:                                                   # Если нет такой директории, то...
            obj = Directory()
            directories_in.append(obj)                          # Вывод на окно
            obj.table_head()
            obj.redraw()
            row += 1                                            # Переход на след. строку


def set_out_dir():
    global row, directories_in
    directory_out = filedialog.askdirectory()               # Открываем диалоговое окно
    if directory_in:                                        # Если папка была выбрана, то...
        for item in directories_in:                             # ...листаем уже выбранные директории
            if directory_out == item.label_in_dir["text"]:          # Если такая директория уже добавлена, то...
                break                                                   # ...пропуск
        else:                                                   # Если нет такой директории, то...
            directories_in.append(Directory())
            row += 1                                                # Переход на след. строку


def about_program():
    global window_about_program, window_height, window_width
    if window_about_program:
        window_about_program.destroy()                          # Удаляем окно, если оно уже существовало
    window_about_program = Toplevel()
    window_about_program.title("О программе")
    window_about_program.geometry(f'600x200+{window_width // 2 - 300}+{window_height // 2 - 100}')
    window_about_program.resizable(False, False)
    Label(window_about_program, text="Music Sorted\n"
                                     "Программа для сортировки музыкальных файлов по их тегам").pack(expand=1)
    Label(window_about_program, text="https://github.com/ig-rudenko/music_sorted")


def start_sort():
    for iteration in directories_in:
        if iteration.label_out_dir["text"]:
            pass
        else:
            messagebox.showerror("", "Укажите для всех директорий папку для переноса")
            break


if __name__ == "__main__":

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

    window_about_program = ''

    window = Tk()
    window.title("Music sorted")
    window_width = window.winfo_screenwidth()       # ширина экрана
    window_height = window.winfo_screenheight()     # высота экрана
    window.geometry(f'800x300+{window_width // 2 - 400}+{window_height // 2 - 150}')    # Расположение по центру экрана
    menu = Menu(window)

    item_1 = Menu(menu, tearoff=0)
    menu.add_cascade(label='Сортировка', menu=item_1)
    item_1.add_command(label='Выполнить сортировку', command=start_sort)
    item_1.add_command(label='Выбрать папку', command=open_folder)
    item_1.add_separator()
    item_1.add_command(label='Выход', command=sys.exit)

    item_2 = Menu(menu, tearoff=0)
    menu.add_cascade(label='Сканирование', menu=item_2)
    item_2.add_command(label='Полное сканирование', command=open_folder)

    item_3 = Menu(menu, tearoff=0)
    menu.add_cascade(label='Информация', menu=item_3)
    item_3.add_command(label='О программе', command=about_program)

    window.config(menu=menu)

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Директории')
    tab_control.add(tab2, text='Статус')
    tab_control.pack(expand=1, fill='both')

    label_tab2 = Label(tab2, text="Нет данных")
    label_tab2.grid(column=1, row=row, sticky=W)

    window.mainloop()

