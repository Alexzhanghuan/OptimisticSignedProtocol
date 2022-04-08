from web3.auto import w3
from web3 import Web3
from eth_account.messages import encode_defunct
from eth_utils.curried import to_hex, to_bytes

def message_process(plain_message_str):
    plain_message = plain_message_str.split()
    empty_message = []
    for x in plain_message:
         empty_message.append(int(x,16))
    hex_plain_message = [hex(x) for x in empty_message]
    return hex_plain_message

def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b"\0"))

def sign_message(message, private_key):
    message = encode_defunct(hexstr=message)
    signed_message = w3.eth.account.sign_message(message, private_key)
    return signed_message