import logging
import threading
from time import perf_counter_ns

class Timer:
    def __init__(self, stage_name: str, interval: int = 10):
        self.stage_name = stage_name
        self.interval = interval
        self._stop_event = threading.Event()

    def __enter__(self):
        self.start_time = perf_counter_ns()
        logging.info(f"Этап {self.stage_name} начат")
        self._thread = threading.Thread(target=self._log_progress, daemon=True)
        self._thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Останавливаем поток
        self._stop_event.set()
        if self._thread:
            self._thread.join()

        elapsed_time = perf_counter_ns() - self.start_time
        logging.info(f"Этап {self.stage_name} выполнялся {elapsed_time / 1e9:.2f} секунд")

    def _log_progress(self):
        while not self._stop_event.wait(self.interval):
            elapsed_time = perf_counter_ns() - self.start_time
            logging.info(
                f"Этап {self.stage_name} длится уже {elapsed_time / 1e9:.2f} секунд"
            )