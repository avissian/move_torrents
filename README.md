### Реализация перемещения раздач для 
* qBittorrent 4.1+
* transmission 3.00 (вероятно, на более старых версиях тоже должно работать)

### Запуск

#### Внести настройки в config.yml:
* блок client:
  * client - qBittorrent или transmission. Если не указан, то qBittorrent
  * host - если не указан, то http://localhost
  * port - если не указан, то 8080
* блок do:
  * new_path - путь перемещения раздач
  * regexp - регулярное выражение, которому должен соответствовать комментарий раздачи, первая группа соответствия добавляется к new_path 
  
#### Подготовка среды для запуска 
Создание virtualenv pyhon: `python -m venv venv`

Linux, активация virtualenv: `. ./venv/bin/activate` 

Windows, активация virtualenv: `.\venv\Scripts\activate`

Установка необоходимых пакетов: `pip install -r requirements.txt`

Запуск `python main.py`

### Результат выполнения

Пример:
```
move Name to /mnt/data/rutracker
skip Name

Skipped: 1
```

Строки, начинающиеся на move - успешно перенесённые раздачи.

Начинающиеся на skip - комментарий в раздаче не соответствует регулярному выражению, не перемещены

Строка в самом конце "Skipped" добавляется, если есть хоть одна пропущенная раздача