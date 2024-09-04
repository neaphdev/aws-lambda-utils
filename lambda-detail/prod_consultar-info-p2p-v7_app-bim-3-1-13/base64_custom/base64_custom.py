import base64
import json

def encode_b64(message):
    if type(message) == bytes:
        base64_bytes = base64.b64encode(message)
    else:
        base64_bytes = base64.b64encode(bytes(message, "utf-8"))
    base64_message = base64_bytes.decode("utf-8")
    return base64_message


def decode_b64(base64_message, encryptation = False):
    base64_bytes = base64_message.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    if encryptation:
        return message_bytes
    message = message_bytes.decode('utf-8')
    return message

def user_pass(base64_message):
    a=decode_b64(base64_message[6:])
    a=a.split(':')
    return a