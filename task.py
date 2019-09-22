import os
import fcntl
import sys
import json
from pathlib import Path
from config import MAX_KEY_SIZE, MAX_FILE_SIZE, MAX_VALUE_SIZE


class FileTask:
    def __init__(self, file_path=None):
        """
        Create file and lock it.

        :param file_path: optional path of a file where data will be stored.
        """
        if file_path is not None:
            self.__file_path = r""+str(file_path)
        else:
            self.__file_path = r""+str(Path.home())
            print("File path not provided therefore creating at location: {}".format(self.__file_path))

        self.__file_path = os.path.join(self.__file_path, "data")
        self.__file_obj = open(self.__file_path, "a+")
        self.__lock_file()

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        """
        overriding magic method to release the file lock.
        :param exc_type: None
        :param exc_value: None
        :param traceback: None
        """
        self.__file_obj.flush()
        os.fsync(self.__file_obj.fileno())
        self.__unlock_file()
        self.__file_obj.close()

    def create_record(self, key, value):
        """
        Method to create a record into file.
        :param key: Key of a record.
        :param value: Value of a record.
        :return: Error string if record ot created else Success string.
        """
        if len(key) <= 0:
            return "ERROR: Invalid key is passed"
        if len(key) > MAX_KEY_SIZE:
            return "ERROR: The maximum size of key can be 32 char long."
        if sys.getsizeof(value) > MAX_VALUE_SIZE:
            return "ERROR: value must be less than or equal to 16 KB"

        if not self.__is_already_available(key):
            value = json.loads(value)
            data = {key: value}
            json_data = json.dumps(data)

            self.__file_obj.write(json_data+"\n")
            self.__file_obj.flush()
            os.fsync(self.__file_obj.fileno())

            if os.path.getsize(self.__file_path) > MAX_FILE_SIZE:
                self.delete_record(key=key)
                return "ERROR: Record not inserted to file because file size is exceeding from 1 GB"

            return "SUCCESS: Record with key {} inserted into file successfully".format(key)

        else:
            return "ERROR: Data with key {} is already available".format(key)

    def delete_record(self, key):
        """
        Delete a record if valid key is given.
        :param key: Key of a record which needs to be deleted.
        :return: Success string if deleted successfully else Error string.
        """
        self.__file_obj.seek(0, os.SEEK_SET)
        records = self.__file_obj.readlines()
        self.__file_obj.seek(0)
        self.__file_obj.truncate()
        found_flag = None
        for record in records:
            data = json.loads(record)
            if list(data.keys())[0] != str(key):
                self.__file_obj.write(record)
                if found_flag is not True:
                    found_flag = False
            else:
                found_flag = True
            self.__file_obj.truncate()

        if found_flag:
            return "SUCCESS: Record with key {} successfully deleted".format(key)
        else:
            return "ERROR: No record found with key {}".format(key)

    def __is_already_available(self, key):
        """
        Check if a record with given key is already available.
        :param key: key of a record whose existence need to be checked.
        :return: True if available else False
        """
        self.__file_obj.seek(0, os.SEEK_SET)
        for record in self.__file_obj:
            record_data = json.loads(record)
            if list(record_data)[0] == str(key):
                return True
        return False

    def read_records(self, key=None):
        """
        Read a record from a file.
        :param key: Key of a record that need to be read.
        :return: Error string on failure else json object.
        """
        self.__file_obj.seek(0, os.SEEK_SET)
        for record in self.__file_obj:
            record_data = json.loads(record)

            record_key = list(record_data)[0]
            record_value = record_data[record_key]

            if record_key == str(key):
                self.__file_obj.seek(0, os.SEEK_END)
                return json.dumps(record_value)

        return "ERROR: No record found with key {}".format(key)

    def get_file_path(self):
        """
        this method will return the path of file being used by current process.
        :return: <str> path of a file
        """
        return self.__file_path

    def __lock_file(self):
        """
        Method to lock the file.
        """
        try:
            fcntl.flock(self.__file_obj, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as e:
            print("Error Number: {}\nError message: {}".format(e.errno, e.strerror))
            print("File is being used by another process.")
            exit(1)

    def __unlock_file(self):
        """
        Method to unlock a file.
        """
        fcntl.flock(self.__file_obj, fcntl.LOCK_UN)
