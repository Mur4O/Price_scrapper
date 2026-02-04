import shutil

# Поиск пути к исполняемому файлу chrome
chrome_path = shutil.which("Google Chrome for Testing")
if chrome_path:
    print(f"Chrome найден: {chrome_path}")
else:
    print("Chrome не найден")
    
