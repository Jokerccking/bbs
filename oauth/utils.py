import time


def log(*args, **kwargs):
    """
    输出到日志文件 oauth.log
    :param args:
    :param kwargs:
    :return:
    """
    f = "%Y/%m/%d %H:%M:%S"
    t = time.strftime(f, time.localtime(int(time.time())))
    with open('oauth.log', 'a', encoding='utf-8') as f:
        print(t, *args, file=f, **kwargs)
