// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
}

contract Faucet {
    address public token;
    uint256 public dripAmount = 1000 * 1e18;
    mapping(address => uint256) public lastClaim;

    constructor(address _token) {
        token = _token;
    }

    function claim() external {
        require(block.timestamp - lastClaim[msg.sender] > 1 hours, "Wait");
        lastClaim[msg.sender] = block.timestamp;
        require(IERC20(token).transfer(msg.sender, dripAmount), "Faucet transfer failed");
    }

    function setDripAmount(uint256 newAmount) external {
        // simple; add onlyOwner if needed
        dripAmount = newAmount;
    }
}
