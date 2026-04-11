#!/bin/bash

# Переход в папку проекта
cd src/Price_scrapper

# Активация виртуального окружения
source .venv/bin/activate

# Запуск скрипта с логированием
python3 src/Python/api.py >> output.log 2>&1