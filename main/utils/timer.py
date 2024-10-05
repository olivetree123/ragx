import time


class Timer(object):

    def __init__(self, name=""):
        self.name = name
        self.start_time = 0

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        t = round(time.time() - self.start_time, 3)
        print(f"[{self.name}]耗时：{t}s")
