const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  const tokenA = "0xFDAKAddress"; // FDAK
  const tokenB = "0xFXAddress";   // FX or stable

  const Router = await hre.ethers.getContractFactory("SwapRouter");
  const router = await Router.deploy(tokenA, tokenB);

  await router.deployed();
  console.log("SwapRouter deployed to:", router.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
