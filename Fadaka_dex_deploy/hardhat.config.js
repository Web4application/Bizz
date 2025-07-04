require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.19",
  networks: {
    fadaka: {
      url: "https://rpc.fadaka.network",
      accounts: ["0xYourPrivateKey"] // Replace with deployer key or use dotenv
    }
  }
};
