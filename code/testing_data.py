

# def websocket_send_audio_data(audio_data):
#     # Websocket will send this message to correct place
#     send_data = {
#         'sender_id': sender_id,
#         ''
#     }
def audio_data(sender_id: str, sending_location: str, audio_data):
    # what something will send to the websocket server
    data = {
        'function_call': 'send_to',
        'sender_id': sender_id,
        'sending_location': sending_location,
        'audio_data': audio_data,
    }
    return data


def speech_to_text(sender_id: str, sending_location: str, speech_to_text):
    # what something will send to the websocket server
    data = {
        'function_call': 'send_to',
        'sender_id': sender_id,
        'sending_location': sending_location,
        'speech_to_text': speech_to_text,
    }
    return data


def validate_data(data):
    """
    Unit test to validate the server command
    :param data: server command
    :return: 
    """
    assert isinstance(data, dict)
    assert 'sender_id' in data
    assert 'sending_location' in data
    assert 'function_call' in data
    assert isinstance(['sender_id'], list)
    assert isinstance(['sending_location'], list)
    assert isinstance(['function_call'], str)



def validate_is_audio_data(data):
    """
    Validates the server response call for Audio_data
    :param data: The server response call
    :return:
    """
    validate_data(data)
    assert 'audio_data' in data





def test_data2():
    data = {
        'function_call': 'send_to',
        'sender_id': ['main_server'],
        'sending_location': 'phone',
        'audio_data': audio_data,
    }
    return data