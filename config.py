import json

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open("data/accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open("data/abi.json", "r") as file:
    ACROSS_ABI = json.load(file)

SPOKE_POOL_ADDRESSES = {
    "zksync": "0xE0B015E54d54fc84a6cB9B666099c46adE9335FF",
    "arbitrum": "0xe35e9842fceaca96570b734083f4a58e8f7c5f2a",
    "optimism": "0x6f26Bf09B1C792e3228e5467807a900A503c0281",
    "base": "0x09aea4b2242abc8bb4bb78d537a67a245a7bec64",
}

CHAIN_IDS = {
    "zksync": 324,
    "arbitrum": 42161,
    "optimism": 10,
    "base": 8453,
}

TOKEN_CONTRACTS = {
    "zksync": {
        "ETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
        "WETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
        "USDC": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDT": "0x493257fd37edb34451f62edf8d2a0c418852ba4c",
        "BUSD": "0x2039bb4116b4efc145ec4f0e2ea75012d6c0f181",
        "MATIC": "0x28a487240e4d45cff4a2980d334cc933b7483842",
        "OT": "0xd0ea21ba66b67be636de1ec4bd9696eb8c61e9aa",
        "MAV": "0x787c09494ec8bcb24dcaf8659e7d5d69979ee508",
        "WBTC": "0xbbeb516fb02a01611cbbe0453fe3c580d7281011",
    },
    "arbitrum": {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    },
    "optimism": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006",
        "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
    },
    "base": {
        "ETH": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
        "WETH": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
        "USDT": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    }
}

UINT256_MAX_UINT = 2 ** 256 - 1
MAX_WAIT_TIME = 180 