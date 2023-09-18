import json
import random
import time

import requests
from loguru import logger
from web3 import Web3
from eth_account import Account as EthereumAccount
from web3.exceptions import TransactionNotFound

from config import ZKSYNC_SPOKE_POOL_ADDRESS, ZKSYNC_TOKENS, ACROSS_ABI, RPC, UINT256_MAX_UINT


class Across:
    def __init__(self, private_key: str, account_index) -> None:
        self.account_id = account_index
        self.private_key = private_key
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

        self.chain = 'zksync'
        self.explorer = RPC[self.chain]["explorer"]
        self.token = RPC[self.chain]["token"]
        self.w3 = Web3(Web3.HTTPProvider(RPC['zksync']["rpc"]))

        self.suggested_fees_base_api = 'https://across.to/api/suggested-fees'

        self.contract = self.w3.eth.contract(address=Web3.to_checksum_address(ZKSYNC_SPOKE_POOL_ADDRESS), abi=ACROSS_ABI)

        self.chain_ids = {
            "optimism": 10,
            "arbitrum": 42161,
        }

    def get_tx_data(self, amount: int):
        tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "value": amount
        }
        return tx

    def calculate_suggested_fees(self, amount, to_chain):
        params = {
            'token': ZKSYNC_TOKENS['WETH'],
            'destinationChainId': self.chain_ids[to_chain],
            'amount': amount,
        }
        response = requests.get(self.suggested_fees_base_api, params)
        if response.status_code == 200:
            parsed_data = json.loads(response.text)
            timestamp = parsed_data['timestamp']
            relay_fee_pact = parsed_data['relayFeePct']
            return timestamp, relay_fee_pact
        else:
            raise Exception(f'got non 200 status code from across suggested-fees API - {response.status_code}')

    def get_amount(
            self,
            min_amount,
            max_amount,
            all_amount,
            keep_value_from,
            keep_value_to,
    ):
        keep_value = round(random.uniform(keep_value_from, keep_value_to), 5)
        random_amount = round(random.uniform(min_amount, max_amount), 5)
        balance = self.w3.eth.get_balance(self.address) - int(Web3.to_wei(keep_value, "ether"))
        amount_wei = balance if all_amount else Web3.to_wei(random_amount, "ether")
        amount = Web3.from_wei(balance, "ether") if all_amount else random_amount

        return amount_wei, amount, balance
                
    def wait_until_tx_finished(self, hash, max_wait_time=180):
        start_time = time.time()
        while True:
            try:
                receipts = self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    logger.success(f"[{self.account_id}][{self.address}] {self.explorer}{hash} successfully!")
                    return True
                elif status is None:
                    time.sleep(1)
                else:
                    logger.error(f"[{self.account_id}][{self.address}] {self.explorer}{hash} transaction failed!")
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    raise Exception('tx failed')
                time.sleep(1)

    def deposit(self, to_chain: str, min_amount, max_amount, keep_value_from=0, keep_value_to=0, all_amount=False):
        logger.info(f'[{self.address}][{self.account_id}][ACROSS] starting bridge zksync->Arbitrum')
        amount_wei, amount, balance = self.get_amount(
            min_amount,
            max_amount,
            all_amount=all_amount,
            keep_value_from=keep_value_from,
            keep_value_to=keep_value_to
        )
        logger.info(f"[{self.address}] Total Balance is {amount}")
        data = self.calculate_suggested_fees(amount_wei, to_chain)
        if data:
            logger.info(
                f"[{self.address}][ACROSS] bridge to {to_chain} | {amount} ETH"
            )

            timestamp, relay_fee_pact = data
            params = [Web3.to_checksum_address(self.address), Web3.to_checksum_address(ZKSYNC_TOKENS["WETH"]),
                      amount_wei, self.chain_ids[to_chain], int(relay_fee_pact), int(timestamp), b"", UINT256_MAX_UINT]

            transaction = self.contract.functions.deposit(*params).build_transaction(self.get_tx_data(amount_wei))

            gas = self.w3.eth.estimate_gas(transaction)
            gas = int(gas * 1.05)
            transaction.update({"gas": gas})

            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

            txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            return self.wait_until_tx_finished(txn_hash.hex())
        else:
            raise Exception('couldnt fetch across suggested fee')
