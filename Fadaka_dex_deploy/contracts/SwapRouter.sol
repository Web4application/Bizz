// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
}

contract SwapRouter {
    address public tokenA;
    address public tokenB;
    address public owner;
    uint256 public rate = 1e18;

    constructor(address _tokenA, address _tokenB) {
        tokenA = _tokenA;
        tokenB = _tokenB;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function setRate(uint256 newRate) external onlyOwner {
        rate = newRate;
    }

    function swap(uint256 amountIn) external returns (uint256 amountOut) {
        require(amountIn > 0, "Zero amount");
        amountOut = amountIn * rate / 1e18;
        require(IERC20(tokenA).transferFrom(msg.sender, address(this), amountIn), "TransferIn failed");
        require(IERC20(tokenB).transfer(msg.sender, amountOut), "TransferOut failed");
    }

    function withdraw(address token) external onlyOwner {
        IERC20(token).transfer(owner, IERC20(token).balanceOf(address(this)));
    }
}
