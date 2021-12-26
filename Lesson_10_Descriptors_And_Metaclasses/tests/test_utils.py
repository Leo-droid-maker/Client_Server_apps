import unittest
import json
import sys
sys.path.append("..")
from Lesson_10_Descriptors_And_Metaclasses.common.utils import get_data, send_data
from Lesson_10_Descriptors_And_Metaclasses.common.config import (
    RESPONSE,
    ERROR,
    USER,
    ACCOUNT_NAME,
    TIME,
    ACTION,
    PRESENCE,
    ENCODING,
    MAX_PACKAGE_LENGTH,
)


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message

    def recv(self, max_len=MAX_PACKAGE_LENGTH):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_correct_dict_send = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'Leo'
        }
    }

    test_get_dict_200 = {RESPONSE: 200}

    test_get_dict_400 = {
        RESPONSE: 400,
        ERROR: "Bad request"
    }


    def test_send_data_ok(self):
        socket = TestSocket(self.test_correct_dict_send)
        send_data(self.test_correct_dict_send, socket)
        self.assertEqual(socket.encoded_message, socket.received_message)

    def test_send_data_err(self):
        incorrect_dict = 'Incorrect_data'
        socket = TestSocket(self.test_correct_dict_send)
        self.assertRaises(TypeError, send_data, socket, incorrect_dict)

    def test_get_data_200(self):
        test_socket_200 = TestSocket(self.test_get_dict_200)
        get_200 = get_data(test_socket_200)
        self.assertEqual(get_200, self.test_get_dict_200)

    def test_get_data_400(self):
        test_socket_err = TestSocket(self.test_get_dict_400)
        get_err = get_data(test_socket_err)
        self.assertEqual(get_err, self.test_get_dict_400)

    def test_get_wrong_data_type(self):
        test_incorrect_list_send = [{
            ACTION: 'msg',
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }]
        test_socket_err = TestSocket(test_incorrect_list_send)
        with self.assertRaises(ValueError):
            get_data(test_socket_err)

if __name__ == '__main__':
    unittest.main()

