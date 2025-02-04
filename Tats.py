import time
import logging
from time import perf_counter_ns

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")

class Timer:
    def __enter__(self):
        self.start_time = perf_counter_ns()
        return self

    def __exit__(self, type, value, traceback): # self, тип ошибки, значение, след
        elapsed_time = perf_counter_ns() - self.start_time
        logging.info(f'Программа выполнялась {elapsed_time / 1000000000} секунд')

with Timer() as t:
    time.sleep(5)
