import os
from datetime import datetime

'''GLOBAL'''
images_log = '.\\processed_images.txt'


def import_txt():
    log_filename = str(datetime.now().date()) + '.txt'
    with open(log_filename, 'a+') as file:
        file.write(f'PROCESS STARTED @ {datetime.now()} \n')
    return log_filename


def import_last_processed():
    with open(images_log, 'a+') as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line = file.readline()
    return last_line


def log_image(filename: str):
    with open(images_log, 'a+') as file:
        file.write(filename + '\n')


class LoggerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=LoggerMeta):

    def __init__(self):
        self.__name__ = 'LOGGER'
        self.log_file = import_txt()
        self.image_checkpoints = import_last_processed()

    def log_message(self, **kwargs):
        msg: str = ''
        try:
            msg = str(datetime.now())
            for args in kwargs.values():
                msg += ' - ' + args
            with open(self.log_file, 'a+') as file:
                file.write(msg + '\n')
        except:
            print(self.__name__ + 'FAILED WRITING LOG: ' + msg)
