import pandas as pd
from collections import defaultdict, deque
from threading import Lock

class DataStore:
    def __init__(self, max_ticks=10000):
        self.ticks = defaultdict(lambda: deque(maxlen=max_ticks))
        self.lock = Lock()

    def add_tick(self, symbol, tick):
        with self.lock:
            self.ticks[symbol].append(tick)

    def get_ticks(self, symbol):
        with self.lock:
            return list(self.ticks[symbol])

store = DataStore()
