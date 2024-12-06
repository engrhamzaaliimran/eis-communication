from abc import ABC
import threading
import sched
import time
import timeit

class Timer(ABC):
    def __init__(self, rate, function_handle, **kwargs):
        super().__init__(**kwargs)
        # rate in milliseconds
        self.rate = rate
        self.running = False
        self._thread = None
        self._scheduler = sched.scheduler(time.perf_counter, time.sleep)
        self._next_event = None
        self._time_start = None
        self._time_next = None
        self._dt = None
        self._function_handle = function_handle

    def _delay(self):
        if self._time_next is None:
            self._time_next = time.perf_counter() + self.rate / 1000
            return self.rate / 1000
        else:
            self._time_next = self._time_next + self.rate / 1000
            return self._time_next - time.perf_counter()

    def _start_thread(self):
        self._next_event = self._scheduler.enter(self._delay(), 2, self.read_handler)
        self._scheduler.run()

    def setup(self):
        pass

    def start(self):
        self.setup()
        self._thread = threading.Thread(target=self._start_thread)
        self.running = True
        self._thread.start()

    def teardown(self):
        pass

    def stop(self):
        if self._next_event is not None:
            self._scheduler.cancel(self._next_event)
            self._next_event = None
        self.running = False
        if self._thread:
            self._thread.join()
            self._thread = None
        self.teardown()

    def read_handler(self):
        self._next_event = self._scheduler.enter(self._delay(), 2, self.read_handler)
        self._function_handle()




