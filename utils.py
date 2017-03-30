import time


def log(*args, **kwargs):
    f = '%Y %m %d"'
    tm = time.localtime(int(time.time()))
    t = time.strftime(f, tm)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(t, *args, file=f, **kwargs)
