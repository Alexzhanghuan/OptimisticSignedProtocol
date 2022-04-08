# OptimisticSignedProtocol
Description:
--------
This protocol aims to develop a fair exchange smart contract with low overhead and gas cost as less as possible.\
You can use it to exchange some secret information in blockchain and others get paid on the countrary.This project also stimulates the fair exchange on blockchain and tests the possible gas cost.\
It corresponds to the paper in the SCIS2022 "Comparison of transaction cost on different fair exchange protocols"\

There remains some parts to be finished.

How to Install and Run the Project:
---
It was wirtten based on the brownie:\
(if you haven't install pipx):
```console
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
Install brownie:
```console
pipx install eth-brownie
```
After you install brownie,you can try to test the pessimistic case and the optimistic case under test net.
```console
brownie run pessimistic_case.py
```
