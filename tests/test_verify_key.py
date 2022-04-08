from brownie import OptiSmartContract, accounts, config
from web3 import Web3


def test_verify_key():
    seller = accounts[0]
    opti_sc = OptiSmartContract.deploy({"from": seller})
    buyer = accounts[1]
    entrance_fee = Web3.toWei(1, "ether")
    opti_sc.transferMoney({"from": buyer, "value": entrance_fee})
    opti_sc.verifyKey(
        0x60298F78CC0B47170BA79C10AA3851D7648BD96F2F8E46A19DBC777C36FB0C00,
        {"from": seller},
    )
