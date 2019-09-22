import os
import fcntl
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyClass:#(object, metaclass=Singleton):
    def __init__(self, file_path=None):
        if file_path is not None:
            self.__file_path = r""+file_path
            self.__file_path = os.path.join(self.__file_path, "data")
            self.__file_obj = open(self.__file_path, "w+")
            self.__lock_file()
            print("Using file".format(self.__file_path))
        else:
            self.__file_path = None
            print("File path not provided therefore creating at location: {}".format(self.__file_path))

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.__file_obj.flush()
        os.fsync(self.__file_obj.fileno())
        self.__unlock_file()
        self.__file_obj.close()

    def do_work(self):
        for i in range(20):
            print("Value of I: {}".format(i))
            time.sleep(5)

    def get_file_path(self):
        print("File path is: {}".format(self.__file_path))

    def __lock_file(self):
        try:
            fcntl.flock(self.__file_obj, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as e:
            print("Error Number: {}\nError message: {}".format(e.errno, e.strerror))
            print("File is being used by another process.")
            exit(1)

    def __unlock_file(self):
        fcntl.flock(self.__file_obj, fcntl.LOCK_UN)
