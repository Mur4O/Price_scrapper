import os
import Python.ImagesFromTPU as ImagesFromTPU

# Выставляем рабочую директорию
base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)

ImagesFromTPU.download_images_from_tpu()