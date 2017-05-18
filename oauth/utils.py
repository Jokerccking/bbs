import time


def log(*args, **kwargs):
    f = "%Y/%m/%d %H:%M:%S"
    t = time.strftime(f, time.localtime(int(time.time())))
    with open('register.log', 'a', encoding='utf-8') as f:
        print(t, *args, file=f, **kwargs)
