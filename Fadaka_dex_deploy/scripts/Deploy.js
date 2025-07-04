const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const FDAK = "0xYourFDAKTokenAddress"; // <- Replace with FDAK proxy
  const FX = await hre.ethers.deployContract("FXToken");
  await FX.waitForDeployment();
  console.log("✅ FXToken:", FX.target);

  const Router = await hre.ethers.deployContract("SwapRouter", [FDAK, FX.target]);
  await Router.waitForDeployment();
  console.log("✅ SwapRouter:", Router.target);

  const FaucetFDAK = await hre.ethers.deployContract("Faucet", [FDAK]);
  await FaucetFDAK.waitForDeployment();
  console.log("✅ FaucetFDAK:", FaucetFDAK.target);

  const FaucetFX = await hre.ethers.deployContract("Faucet", [FX.target]);
  await FaucetFX.waitForDeployment();
  console.log("✅ FaucetFX:", FaucetFX.target);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
