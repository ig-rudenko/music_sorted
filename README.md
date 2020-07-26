# Music Sorted

Программа для сортировки музыкальных сборок по их тегам:
* Артист
* Год выпуска альбома
* Название альбома

Воспринимает только .flac и .mp3 формат музыкальных файлов

`/dist`     - находится .exe файл, для запуска на ОС Windows 

`/mutagen`  - содержит в себе модуль Python для обработки звуковых метаданных

# Описание
Сортировке подлежат все файлы, находящиеся в сборниках, а не только имеющие музыкальный формат

Программе передается полный путь до папки, в которой хранятся сборники с музыкой.

На выходе получаем 2 папки:
* Compilations
* Artist_Album
# Compilations
В данную папку помещаются сборки, в которых находятся музыкальные файлы с разными тегами альбомов
# Artist_Album
Данная папка содержит в себе папки с артистами, в которых, в свою очередь, находятся папки с альбомами в формате: 

["год выпуска альбома"] "название альбома"
#
