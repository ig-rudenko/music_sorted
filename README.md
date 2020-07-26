# Music Sorted

Программа для сортировки музыкальных сборок по их тегам:
* Артист
* Год выпуска альбома
* Название альбома

Воспринимает только `.flac` и `.mp3` формат музыкальных файлов

`/dist`     - находится `.exe` файл, для запуска на ОС Windows 

`/mutagen`  - содержит в себе модуль Python для обработки звуковых метаданных

# Описание
Предоставляется два вида сортировки:
* каждый файл отдельно
* как 'сборник'

В первом случае обрабатывается каждый файл по отдельности и на основе его собственных тегов определяется папка для сортировки. При такой сортировке учитываются только `.flac` и `.mp3` файлы. 

Сортировке подлежат все файлы, находящиеся в сборниках, а не только имеющие музыкальный формат

Программе передается полный путь до папки, в которой хранятся сборники с музыкой.

На выходе получаем 2 папки:
* Compilations

В данную папку помещаются сборки, в которых находятся музыкальные файлы с разными тегами альбомов

* Artist_Album

Данная папка содержит в себе папки с артистами, в которых, в свою очередь, находятся папки с альбомами в формате: 

["год выпуска альбома"] "название альбома"
#
