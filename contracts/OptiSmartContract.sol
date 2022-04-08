// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

contract OptiSmartContract {
    uint256 constant length = 128;
    address payable public seller;
    address payable public buyer = 0xF011A0d3A5B92F4378F06cAF37045a7cBDB0Fe9F;
    bytes32 public keyCommit =
        0x81ed425f493c145750182ff2589ba232235d9ba9512e639d6e40392cccbd4371;
    bytes32 public key;
    uint256 public timeout;
    uint256 public price = 1000000000000000000; //wei
    bytes32 public hash_plain_text = 0x1154e74b621202f1bcae1e517ba8eddad7f3868c3eb15c7855b02bd3bd41c035;
    enum STAGE {
        created,
        initialize,
        revealKey
    }
    STAGE public stage = STAGE.created;

    constructor() public {
        //可以在这里验证 verify(sig,pk_s,ct)
        timeout = now + 10 seconds;
        seller = msg.sender;
    }

    modifier allowed(address p, STAGE s) {
        require(msg.sender == p);
        require(stage == s);
        _;
    }

    function transferMoney() public payable allowed(buyer, STAGE.created) {
        require(msg.value >= price, "This is not enough!");
        stage = STAGE.initialize;
        timeout = now + 10 seconds;

    }

    function verifyKey(bytes32 _key) public allowed(seller, STAGE.initialize) {
        if (keyCommit == keccak256(abi.encodePacked(_key)) && now <= timeout) {
            stage = STAGE.revealKey;
            key = _key;
            timeout = now + 10 seconds;
        } else {
            selfdestruct(buyer);
        }
    }

    function complain(bytes32[length] memory _cipherText, bytes32 _messageHash, uint8 v, bytes32 r, bytes32 s) 
    public allowed(buyer, STAGE.revealKey) payable {
        require(verifySignature( _messageHash, v, r, s) == true,"this is the wrong signature");
        require(predicate(decrypt(_cipherText))==false,"This is the right file");
        selfdestruct(buyer);
    }
        
    function noComplain() public allowed(buyer, STAGE.revealKey) {
        selfdestruct(seller);
    }

    function refund() public payable{
        require(now>timeout,"Please call it later!");
        if(stage ==STAGE.created) selfdestruct(seller);
        if(stage == STAGE.initialize) selfdestruct(buyer);
        if(stage == STAGE.revealKey) selfdestruct(seller);

    }

    function verifySignature(bytes32 _messageHash, uint8 v, bytes32 r, bytes32 s) internal view returns(bool){
        address signer = ecrecover(_messageHash, v,r,s);
        return  signer == seller;
    }

    function predicate(bytes32[length] memory _plainMessageHash) internal view returns(bool)  {
        return hash_plain_text==keccak256(abi.encode(_plainMessageHash));
        //return keccak256(abi.encode(_plainMessageHash));
    }
    function decrypt(bytes32[length] memory _ciphertext) public view returns(bytes32[length] memory) {
        uint256 _index = 0;
        for (uint256 i = 0; i < length; i++) {
            _ciphertext[i] = keccak256(abi.encode(_index, key)) ^ _ciphertext[i];
            _index++;
        }
        return _ciphertext;
    }

}
