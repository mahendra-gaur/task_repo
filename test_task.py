import unittest
from task import FileTask
from pathlib import Path
import os
import json


class TestFileTask(unittest.TestCase):
    def setUp(self):
        """
        create file, this method will be invoked before running each test case.
        """
        self.actual_file_path = os.path.join(r"" + str(Path.home()), "data")
        self.task_obj = FileTask(Path.home())

    def test_file_creation(self):
        """
        Test case to check if file is created at the given location or not.
        """
        if os.path.exists(self.actual_file_path):
            self.assertTrue(os.path.isfile(self.actual_file_path))

    def test_create_record_success(self):
        """
        Test case to test create records.
        """
        key = 'test_key'
        value = {"First Name": "Mahendra", "Last Name": "Gaur", "unique_key": key}
        value = json.dumps(value)
        expected_response = "SUCCESS: Record with key {} inserted into file successfully".format(key)
        actual_response = self.task_obj.create_record(key=key, value=value)
        self.assertEqual(actual_response, expected_response)

    def test_create_record_with_existing_key(self):
        """
        Test case to test create record with existing key.
        """
        key = 'test_key'
        value = {"First Name": "Mahendra", "Last Name": "Gaur", "unique_key": key}
        value = json.dumps(value)
        self.task_obj.create_record(key=key, value=value)

        value = {"First Name": "Mahendra", "Last Name": "Gaur", "unique_key": key}
        value = json.dumps(value)
        actual_response = self.task_obj.create_record(key=key, value=value)
        expected_response = "ERROR: Data with key {} is already available".format(key)
        self.assertEqual(actual_response, expected_response)

    def test_create_with_invalid_key(self):
        """
        Test case to test create record with invalid key.
        """
        key = str('')
        value = {"First Name": "Mahendra", "Last Name": "Gaur"}
        value = json.dumps(value)
        actual_response = self.task_obj.create_record(key=key, value=value)
        expected_response = "ERROR: Invalid key is passed"
        self.assertEqual(actual_response, expected_response)

    def test_create_with_key_size_mote_than_32_char(self):
        """
        Test case to test create record with key size more than 32 characters.
        """
        key = 'TESTTESTTESTTESTTESTTESTTESTTESTT'
        value = {"First Name": "Mahendra", "Last Name": "Gaur"}
        value = json.dumps(value)
        actual_response = self.task_obj.create_record(key=key, value=value)
        expected_response = "ERROR: The maximum size of key can be 32 char long."
        self.assertEqual(actual_response, expected_response)

    def test_read_record_success(self):
        """
        Test case to test read record Successfully.
        """
        key = 'test_key'
        value = {"First Name": "Mahendra", "Last Name": "Gaur"}
        expected_response = json.dumps(value)
        value = json.dumps(value)
        self.task_obj.create_record(key=key, value=value)
        actual_response = self.task_obj.read_records(key=key)
        self.assertEqual(actual_response, expected_response)

    def test_read_record_failure(self):
        """
        Test case to test read record failure.
        """
        key = 'test_key'
        value = {"First Name": "Mahendra", "Last Name": "Gaur"}
        value = json.dumps(value)
        self.task_obj.create_record(key=key, value=value)
        expected_response = "ERROR: No record found with key {}".format("123")
        actual_response = self.task_obj.read_records(key='123')
        self.assertEqual(actual_response, expected_response)

    def test_delete_record_success(self):
        """
        Test case to test delete records successfully.
        """
        key = 'test_key'
        value = {"First Name": "Mahendra", "Last Name": "Gaur", "unique_key": key}
        value = json.dumps(value)
        self.task_obj.create_record(key=key, value=value)

        expected_response = "SUCCESS: Record with key {} successfully deleted".format(key)
        actual_response = self.task_obj.delete_record(key=key)

        self.assertEqual(actual_response, expected_response)

    def test_delete_record_failure(self):
        """
        Test case to test failure of delete record.
        """
        key = "123"
        expected_response = "ERROR: No record found with key {}".format(key)
        actual_response = self.task_obj.delete_record(key=key)

        self.assertEqual(actual_response, expected_response)

    def tearDown(self):
        """
        Deleting file, This method will be invoked after each test case.
        """
        os.remove(self.actual_file_path)


if __name__ == '__main__':
    unittest.main()
