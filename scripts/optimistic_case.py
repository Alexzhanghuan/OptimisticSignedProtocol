from brownie import OptiSmartContract, accounts, config
from dotenv import load_dotenv
from web3 import Web3
from scripts.helpful_scripts import message_process,to_32byte_hex,sign_message

def optimistic_case():

    #1.deploy this contract
    seller = accounts[0]
    buyer = accounts[1]
    opti_sc = OptiSmartContract.deploy({"from": seller})

    #2.seller construct signature and cipher text
    private_key = 0xfc428b8a0bc40b84ff74d1a13cbad1972518751266f9f51a8e327ed5859c5c26
    plain_message_str = 'ba ba ba bab abab ababab ababa baba baba bababa bababab ababababab ababa babab ba ba  ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba baba ba abab aba ba ba ba ba ba ba ba ba ba ba ba bab abab ababab ababa baba baba bababa bababab ababababab ababa babab ba ba  ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba ba baba ba abab aba ba ba ba ba ba ba ba ba'
    hex_plain_message = message_process(plain_message_str)
    #hashed_msg is the hashed value of hex_plain_message
    hashed_msg = '0x42e931e775535d47c0a0b73ee50e279fd0ff357d06b2fd069147bccaa738a5b8'
    signed_message = sign_message(hashed_msg,private_key)

    (msghash, v, r, s) = (
        Web3.toHex(signed_message.messageHash),
        signed_message.v,
        to_32byte_hex(signed_message.r),
        to_32byte_hex(signed_message.s),
    )
    #get the cipher text
    cipher_text = opti_sc.decrypt(hex_plain_message)
    

    #3.buyer transfer money to this smart contract
    entrance_fee = Web3.toWei(1, "ether")
    opti_sc.transferMoney({"from": buyer, "value": entrance_fee})

    #4.seller reveal key
    opti_sc.verifyKey(
        0x60298F78CC0B47170BA79C10AA3851D7648BD96F2F8E46A19DBC777C36FB0C00,
        {"from": seller},
    )
    #5.buyer accept
    opti_sc.noComplain({"from":buyer})
    #opti_sc.complain(cipher_text,msghash,v,r,s,{"from":buyer})

def main():
    optimistic_case()