import os

# Выставляем рабочую директорию
base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)

# Получить имя текущей директории
dir = os.path.dirname(os.path.abspath(__file__))
print(dir)
# СОбрать путь до файла
output_path = os.path.join(dir, 'Other', 'DNS')

with open(output_path, 'r', encoding='utf-8') as f:
    file = f.readlines()
    for line in file:
        print(line)
        