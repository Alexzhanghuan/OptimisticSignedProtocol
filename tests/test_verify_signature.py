from brownie import OptiSmartContract, accounts, config
from web3.auto import w3
from eth_account.messages import encode_defunct
import os
from dotenv import load_dotenv
from web3 import Web3
from eth_utils.curried import to_hex, to_bytes


# automatically import env doc
load_dotenv()

def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b"\0"))

def test_verify_signature():
    seller = accounts[0]
    buyer = accounts[1]
    opti_sc = OptiSmartContract.deploy({"from": seller})

    private_key = 0xFC428B8A0BC40B84FF74D1A13CBAD1972518751266F9F51A8E327ED5859C5C26
    plain_message = 'We have two main parties: the seller and the buyer in this process. The seller owns the commodity and is willing to sell it to someone paying a predefined price. In contrast, the buyer wants to buy something by paying the price of this good. There are two kinds of misbehaviors in previous situations: (a)the sender might refuse to send the goods or send the wrong one to the receiver after he gets paid. In another case. (b)the bad receiver may leave without paying money to the sender once he receives the good. But it is hard to guarantee the fairness that the seller gets the money if he sends the right good and the buyer gets good after successfully sending money to the sender. According to Asokans definition, this kind strong fairness [4]. Based on the difficulty of keeping fairness, people try to introduce a third party acting as a judge to support the fairness exchange. However, always reliable to find an appropriate third party.'
    hex_bytes = binascii.hexlify(plain_message.encode('cp1252')) 
    msg = '0x42e931e775535d47c0a0b73ee50e279fd0ff357d06b2fd069147bccaa738a5b8'

    signed_message = sign_message(msg,private_key)
    # signer = w3.eth.account.recover_message(message, signature=signed_message.signature)
    # assert signer == seller

    #deploy smart contract
    

    (msghash, v, r, s) = (
        Web3.toHex(signed_message.messageHash),
        signed_message.v,
        to_32byte_hex(signed_message.r),
        to_32byte_hex(signed_message.s),
    )
    cipher_text = opti_sc.decrypt(plain_message)
    result = opti_sc.complain(cipher_text,msghash,v,r,s,{"from":buyer})
    
    #assert result == 1
    


def sign_message(message, private_key):
    message = encode_defunct(hexstr=message)
    signed_message = w3.eth.account.sign_message(message, private_key)
    return signed_message

# def verify_signature():



