import json

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open("data/accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open("data/abi.json", "r") as file:
    ACROSS_ABI = json.load(file)

ZKSYNC_SPOKE_POOL_ADDRESS = '0xE0B015E54d54fc84a6cB9B666099c46adE9335FF'

ZKSYNC_TOKENS = {
    "ETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
    "WETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
    "USDC": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
    "USDT": "0x493257fd37edb34451f62edf8d2a0c418852ba4c",
    "BUSD": "0x2039bb4116b4efc145ec4f0e2ea75012d6c0f181",
    "MATIC": "0x28a487240e4d45cff4a2980d334cc933b7483842",
    "OT": "0xd0ea21ba66b67be636de1ec4bd9696eb8c61e9aa",
    "MAV": "0x787c09494ec8bcb24dcaf8659e7d5d69979ee508",
    "WBTC": "0xbbeb516fb02a01611cbbe0453fe3c580d7281011",
}

UINT256_MAX_UINT = 2 ** 256 -1
