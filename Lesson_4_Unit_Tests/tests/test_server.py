import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('../..'))
from Lesson_4_Unit_Tests.common.config import *
from Lesson_4_Unit_Tests.server import create_response


class TestServer(unittest.TestCase):

    def test_correct_data_to_create_response(self):
        test_correct_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Leo'
            },
        }
        correct_response = create_response(test_correct_msg)
        self.assertEqual(correct_response, {RESPONSE: 200})


    def test_incorrect_data_to_create_response(self):
        test_incorrect_msg = {
            ACTION: 'msg',
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            },
        }
        incorrect_response = create_response(test_incorrect_msg)
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
            create_response(test_none_msg)





if __name__ == '__main__':
    unittest.main()
