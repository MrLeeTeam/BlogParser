
import datetime
import sys


def log(msg, *args, **kwargs):
    list = (str(i) for i in args)
    print "[", datetime.datetime.now(), "] : ", msg, " ".join(list)
    sys.stdout.flush()