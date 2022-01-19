Реализация перемещения раздач для qBittorrent 4.1+

### Запуск

Внести настройки в config.yml

```commandline
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python main.py
```

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