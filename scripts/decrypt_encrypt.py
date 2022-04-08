from brownie import OptiSmartContract, accounts, config
from dotenv import load_dotenv
from web3 import Web3
from scripts.helpful_scripts import message_process,to_32byte_hex,sign_message


# automatically import env doc
load_dotenv()



def decrypt_encrypt():
    seller = accounts[0]
    buyer = accounts[1]
    opti_sc = OptiSmartContract.deploy({"from": seller})

    private_key = 0xFC428B8A0BC40B84FF74D1A13CBAD1972518751266F9F51A8E327ED5859C5C26
    plain_message_str = 'ba ba ba bab abab ababab ababa baba baba bababa bababab ababababab ababa babab ba ba  ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba baba ba abab aba ba ba ba ba ba ba ba ba'
    hex_plain_message = message_process(plain_message_str)

    msg = '0x42e931e775535d47c0a0b73ee50e279fd0ff357d06b2fd069147bccaa738a5b8'
    signed_message = sign_message(msg,private_key)

    (msghash, v, r, s) = (
        Web3.toHex(signed_message.messageHash),
        signed_message.v,
        to_32byte_hex(signed_message.r),
        to_32byte_hex(signed_message.s),
    )

    cipher_text = opti_sc.decrypt(hex_plain_message)
    opti_sc.complain(cipher_text,msghash,v,r,s,{"from":buyer})
    
def main():
    decrypt_encrypt()