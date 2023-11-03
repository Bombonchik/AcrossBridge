import json
import random
import time

import requests
from loguru import logger
from web3 import Web3
from eth_account import Account as EthereumAccount
from web3.exceptions import TransactionNotFound

from config import SPOKE_POOL_ADDRESSES, CHAIN_IDS, TOKEN_CONTRACTS, ACROSS_ABI, RPC, UINT256_MAX_UINT, MAX_WAIT_TIME


class Across:
    def __init__(self, from_chain: str, private_key: str, account_index) -> None:
        self.account_id = account_index
        self.private_key = private_key
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

        self.from_chain = from_chain
        self.explorer = RPC[self.from_chain]["explorer"]
        self.token = RPC[self.from_chain]["token"]
        self.w3 = Web3(Web3.HTTPProvider(RPC[self.from_chain]["rpc"]))

        self.suggested_fees_base_api = 'https://across.to/api/suggested-fees'

        self.contract = self.w3.eth.contract(address=Web3.to_checksum_address(SPOKE_POOL_ADDRESSES[self.from_chain]), abi=ACROSS_ABI)

        self.chain_ids = CHAIN_IDS

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
            'token': TOKEN_CONTRACTS[self.from_chain]['WETH'],
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
            logger.error(f"Failed API call. HTTP Status: {response.status_code}, Content: {response.text}")


    def get_amount(
        self,
        min_amount,
        max_amount,
        transfer_all_amount,
        keep_value_from,
        keep_value_to,
    ):
        keep_value = round(random.uniform(keep_value_from, keep_value_to), 5)
        random_amount = round(random.uniform(min_amount, max_amount), 5)
        balance = self.w3.eth.get_balance(self.address)
        all_amount = balance - int(Web3.to_wei(keep_value, "ether"))
        amount_wei = all_amount if transfer_all_amount else Web3.to_wei(random_amount, "ether")
        amount = Web3.from_wei(all_amount, "ether") if transfer_all_amount else random_amount

        return amount_wei, amount, Web3.from_wei(balance, "ether")
                
    def wait_until_tx_finished(self, hash, max_wait_time=MAX_WAIT_TIME):
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

    def deposit(self, to_chain: str, min_amount, max_amount, keep_value_from=0, keep_value_to=0, transfer_all_amount=False):
        logger.info(f'[{self.address}][{self.account_id}][ACROSS] starting bridge {self.from_chain}->{to_chain}')
        amount_wei, amount, balance = self.get_amount(
            min_amount,
            max_amount,
            transfer_all_amount=transfer_all_amount,
            keep_value_from=keep_value_from,
            keep_value_to=keep_value_to
        )
        logger.info(f"[{self.address}] Total Balance is {balance}")
        data = self.calculate_suggested_fees(amount_wei, to_chain)
        if data:
            timestamp, relay_fee_pact = data
            params = [Web3.to_checksum_address(self.address), Web3.to_checksum_address(TOKEN_CONTRACTS[self.from_chain]["WETH"]),
                    amount_wei, self.chain_ids[to_chain], int(relay_fee_pact), int(timestamp), b"", UINT256_MAX_UINT]

            transaction = self.contract.functions.deposit(*params).build_transaction(self.get_tx_data(amount_wei))

            gas = self.w3.eth.estimate_gas(transaction)
            gas = int(gas * 1.05)
            transaction.update({"gas": gas})

            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

            txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            return self.wait_until_tx_finished(txn_hash.hex())
        else:
            raise Exception("Could not fetch Across suggested fee")
