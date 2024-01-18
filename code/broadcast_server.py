"""
Websocket server for raspberry pi

SECURITY CONCERNS:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
READ:
https://superuser.com/questions/561140/how-safe-is-port-forwarding-in-general

A hacker can not access you through the forwarded ports. But your router may be set up to allow configuration on a web
port. How to set this up is different for each router, but make sure anything similar to "allow configuration on WAN"
is disabled. Allow LAN configuration only.
SETUP FIREWALL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
import json

import websockets
import asyncio
from testing_data import validate_data
from keys import decrypt_message
from helpful_functions import create_logger_error
import os

"""
Create cert once on device (not sure how to make this work with the code), could I have it auto create on startup?
"""
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(
#     pathlib.Path(__file__).with_name('cert.pem'),
#     pathlib.Path(__file__).with_name('key.pem')
# )


# Server data
PORT = 7890
print("Server listening on Port " + str(PORT))

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
USE ENVIRONMENT VARIABLES FOR PRODUCTION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
user_credentials = {
    "whisper_server": "whisper_server_password(6543",
    "desktop": "Desktops_are_for_loserz987&",
    "phone": "phone_password",
    "laptop": 'laptop_password#567',
    "api_server": 'API_SERVER_PASSWORD123#',
    "async_thread": "ASYNC_IS_GR8_567%",  # This is the "database checker" thread
}

# A set of connected WebSocket clients
connected = {}


async def main_loop(websocket):
    """
    The main loop of the server
    """
    username_nullable = await authenticate(websocket)
    if isinstance(username_nullable, str):
        print(f"User {username_nullable} just connected")
        try:
            while True:
                async for message in websocket:
                    if message == 'ping':
                        await websocket.send('pong')
                        continue
                    if message == 'api_server':
                        await api_server(websocket)
                    else:
                        await take_in_message(websocket, message)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"User {username_nullable} just disconnected")
            connected.pop(username_nullable)


async def authenticate(websocket) -> str or None:
    """
    authenticate the user
    if something failed will close the websocket
    :param websocket: the websocket connection
    :return: username of the connected or None if failed
    """
    await websocket.send("Please enter your username:")
    username_encrypted = await websocket.recv()
    username = decrypt_message(username_encrypted)

    if username in user_credentials:
        await websocket.send("Please enter your password:")
        password_encrypted = await websocket.recv()
        password = decrypt_message(password_encrypted)

        if user_credentials[username] == password:
            connected[username] = websocket
            await websocket.send("Authentication successful. You are now connected.")
            return username
        else:

            await websocket.send("Authentication failed. Closing connection.")
            await websocket.close()
            return None
    else:
        await websocket.send("User not found. Closing connection.")
        await websocket.close()
        return None


async def api_server(websocket):
    """
    Api server variant
    :param websocket:
    :param message:
    :return:
    """
    while True:
        await asyncio.sleep(10)
        await websocket.send('ping')
        check = await websocket.recv()
        if check != 'pong':
            await websocket.send('ERROR: api server not responding')
            return


async def take_in_message(websocket, message: str):
    logger = create_logger_error(os.path.abspath(__file__), 'take_in_message', log_to_console=True)
    message = json.loads(message)
    logger.info(message)
    try:
        validate_data(message)
    except AssertionError as e:
        await websocket.send('ERROR' + str(e))
    if message['function_call'] == 'send_to':
        await send_to(message=message, sending_location=message['sending_location'])


async def send_to(sending_location: list, message: str):
    for location in sending_location:
        send_to_websocket = connected[location]
        json_string = json.dumps(message)
        await send_to_websocket.send(json_string)


if __name__ == '__main__':
    print('hio')
    start_server = websockets.serve(main_loop, os.getenv("IP"), os.getenv("PORT"))
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
