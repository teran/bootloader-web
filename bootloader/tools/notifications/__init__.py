from bootloader.settings import NOTIFICATION_MODULES
import importlib

class Notification():
    def __init__(self, message):
        for m in NOTIFICATION_MODULES:
            mod = importlib.import_module(m)
            mod.Message(message=message)


class ThirdPartyAPIException(Exception):
    pass
