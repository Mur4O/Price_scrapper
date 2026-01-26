from time import perf_counter_ns
import threading
import logging

class Timer:
    def __init__(self, stage_name: str, interval: int = 10):
        self.stage_name = stage_name
        self.interval = interval
        self.start_time = perf_counter_ns()
        # Объявляем поток, говорим выполнять функцию _log_progress
        self._thread = threading.Thread(target=self._log_progress, daemon=True)
        # Объявляем ивент, при активации ивента (функция set()) останавливается логирование
        self._stop_event = threading.Event()

    def __enter__(self):
        # Запускаем поток
        self._thread.start()
        logging.info(f'Этап {self.stage_name} начат')
        return self

    def __exit__(self, type, value, traceback): # self, тип ошибки, значение, след
        # Выставляем _stop_event в True
        self._stop_event.set()
        elapsed_time = perf_counter_ns() - self.start_time
        logging.info(f'Этап {self.stage_name} выполнялся {elapsed_time / 1000000000} секунд')
        # Join позволяет дождаться завершения потока
        if self._thread:
            self._thread.join()

    def _log_progress(self):
        while not self._stop_event.wait(self.interval):
            elapsed_time = perf_counter_ns() - self.start_time
            logging.info(f'Этап длится {elapsed_time / 1000000000} секунд')