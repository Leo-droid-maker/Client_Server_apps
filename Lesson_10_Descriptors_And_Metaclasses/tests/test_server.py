import unittest
import sys
sys.path.append("..")
from Lesson_10_Descriptors_And_Metaclasses.common.config import *
from Lesson_10_Descriptors_And_Metaclasses.server import create_response_message


class TestServer(unittest.TestCase):

    def test_correct_data_to_create_response(self):
        test_correct_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Leo'
            },
        }
        correct_response = create_response_message(test_correct_msg)
        self.assertEqual(correct_response, {RESPONSE: 200})


    def test_incorrect_data_to_create_response(self):
        test_incorrect_msg = {
            ACTION: 'msg',
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            },
        }
        incorrect_response = create_response_message(test_incorrect_msg)
        self.assertEqual(incorrect_response, {RESPONSE: 400, ERROR: "Bad request"})

    def test_none_data_to_create_response(self):
        test_none_msg = {
            ACTION: None,
            TIME: None,
            USER: {
                ACCOUNT_NAME: None
            },
        }
        with self.assertRaises(ValueError):
            create_response_message(test_none_msg)





if __name__ == '__main__':
    unittest.main()
