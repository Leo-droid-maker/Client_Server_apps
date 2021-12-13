from .config import *
import json
import sys
sys.path.append("..")
from Lesson_7_Socket_Select.decorators import my_log

@my_log
def get_data(socket):
    data = socket.recv(MAX_PACKAGE_LENGTH)
    if isinstance(data, bytes):
        json_data = data.decode(encoding=ENCODING)
        decoded_data = json.loads(json_data)
        if isinstance(decoded_data, dict):
            return decoded_data
        raise ValueError
    raise ValueError

@my_log
def send_data(response_obj, socket):
    js_response = json.dumps(response_obj)
    encoded_response = js_response.encode(encoding=ENCODING)
    socket.send(encoded_response)