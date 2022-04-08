from brownie import OptiSmartContract, accounts, config
from dotenv import load_dotenv
from web3 import Web3
import threading
from scripts.helpful_scripts import message_process,to_32byte_hex,sign_message

#the buyer cannot receive key before time K+D
#D=11 seconds
def abort_in_created():
    seller = accounts[0]
    opti_sc = OptiSmartContract[-1]
    opti_sc.refund({"from":seller})

def abort_in_initialize():
    buyer = accounts[1]
    opti_sc = OptiSmartContract[-1]
    opti_sc.refund({"from":buyer})

def abort_in_reveal_key():
    seller = accounts[0]
    opti_sc = OptiSmartContract[-1]
    opti_sc.refund({"from":seller})

def complain_about_wrong_file():
    buyer = accounts[1]
    opti_sc = OptiSmartContract[-1]
    opti_sc.refund({"from":buyer})


def main():
    #1.deploy this contract
    seller = accounts[0]
    buyer = accounts[1]
    opti_sc = OptiSmartContract.deploy({"from": seller})

    #Abort in created, buyer dosen't transfer moeny in time
    # delay = int(11)
    # start_time = threading.Timer(delay, abort_in_created)  # no brace and no args
    # start_time.start()

    #Abort in waiting key 
    #buyer transfer money to this smart contract
    entrance_fee = Web3.toWei(1, "ether")
    opti_sc.transferMoney({"from": buyer, "value": entrance_fee})
    # delay = int(11)
    # start_time = threading.Timer(delay, abort_in_initialize)  # no brace and no args
    # start_time.start()

    #Abort in doesn't get response from buyer
    # private_key = 0xfc428b8a0bc40b84ff74d1a13cbad1972518751266f9f51a8e327ed5859c5c26
    # plain_message_str = 'ba ba ba bab abab ababab ababa baba baba bababa bababab ababababab ababa babab ba ba  ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba baba ba abab aba ba ba ba ba ba ba ba ba'
    # hex_plain_message = message_process(plain_message_str)
    # msg = '0x42e931e775535d47c0a0b73ee50e279fd0ff357d06b2fd069147bccaa738a5b8'
    # signed_message = sign_message(msg,private_key)

    # (msghash, v, r, s) = (
    #     Web3.toHex(signed_message.messageHash),
    #     signed_message.v,
    #     to_32byte_hex(signed_message.r),
    #     to_32byte_hex(signed_message.s),
    # )
    # cipher_text = opti_sc.decrypt(hex_plain_message)
    opti_sc.verifyKey(
        0x60298F78CC0B47170BA79C10AA3851D7648BD96F2F8E46A19DBC777C36FB0C01,
        {"from": seller},
    )
    # result = opti_sc.complain(cipher_text,msghash,v,r,s,{"from":buyer})
    # print(result)


