import datetime
import os


def DEBUG(*args, **kwargs):
    log_level = os.environ.get("LOG_LEVEL")
    if log_level == "1":
        print("DEBUG({}): {}".format(datetime.datetime.now(), *args, **kwargs))


def ERROR(*args, **kwargs):
    log_level = os.environ.get("LOG_LEVEL")
    if log_level == "1" or log_level == "2":
        print("ERROR({}): {}".format(datetime.datetime.now(), *args, **kwargs))
