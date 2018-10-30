import time


def log(text):
    print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
