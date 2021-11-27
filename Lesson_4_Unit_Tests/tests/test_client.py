import unittest
from Lesson_4_Unit_Tests.common.config import RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
from Lesson_4_Unit_Tests.client import create_answer, create_presence_message_to_server, start_client


class TestClient(unittest.TestCase):

    def test_create_correct_msg(self):
        test = create_presence_message_to_server()

        test[TIME] = 1.1

        test_correct_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Leo'
            },
        }
        self.assertEqual(test, test_correct_msg)

    def test_create_incorrect_action_msg(self):
        with self.assertRaises(ValueError):
            create_presence_message_to_server(action='msg')

    def test_create_incorrect_acc_name_msg(self):
        with self.assertRaises(ValueError):
            create_presence_message_to_server(account_name='Guest')

    def test_200_create_answer(self):
        test_correct_response_obj = {RESPONSE: 200}
        self.assertEqual(create_answer(test_correct_response_obj), '200: OK')

    def test_400_create_answer(self):
        test_incorrect_response_obj = {
            RESPONSE: 400,
            ERROR: "Bad request"
        }
        self.assertEqual(create_answer(test_incorrect_response_obj), '400: Bad request')

    def test_empty_response(self):
        with self.assertRaises(ValueError):
            create_answer({RESPONSE: ''})

    def test_start_client(self):

        with self.assertRaises(Exception):
            start_client()


if __name__ == '__main__':
    unittest.main()
