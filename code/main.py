import websockets
import asyncio
from keys import encrypt_message, decrypt_message
from testing_data import test_data2
from broadcast_server import PORT, main_loop
from helpful_functions import create_logger_error
import os


if __name__ == '__main__':
    print('HELLO')
    logger = create_logger_error(os.path.abspath(__file__), '')
    start_server = websockets.serve(main_loop, "0.0.0.0", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
