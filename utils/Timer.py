from datetime import datetime
from datetime import timedelta


class Timer:
    start_time = None

    def __init__(self):
        self.start_time = datetime.now()

    def get_duration(self):
        return (datetime.now() - self.start_time).seconds

    def time(self):
        return datetime.now().time()

    def time_restart(self,start_time = datetime.now()):
        a,b,c = start_time.year,start_time.month,start_time.day
        d = datetime(a,b,c+1)
        e = d + timedelta(hours=5)
        if start_time.hour < 5:
            e -= timedelta(days=1)
        return [d,e]

if __name__=="__main__":
    import sys
    sys.path.append('./')
    from settings import *

    timer = Timer()
    print(timer.time_restart(datetime(2021,11,14,3,00,00)))