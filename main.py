import random
import time

from loguru import logger

from config import ACCOUNTS
from modules.across import Across
from settings import FROM_CHAIN, TO_CHAIN, AMOUNT_FROM, AMOUNT_TO, TRANSFER_ALL_AMOUNT, KEEP_VALUE_FROM, KEEP_VALUE_TO, SLEEP_FROM, SLEEP_TO, SHUFFLE_WALLETS


def main():
    if SHUFFLE_WALLETS:
        random.shuffle(ACCOUNTS)
    for index, private_key in enumerate(ACCOUNTS):
        across = Across(FROM_CHAIN, private_key, index)
        try:
            across.deposit(TO_CHAIN, AMOUNT_FROM, AMOUNT_TO, KEEP_VALUE_FROM, KEEP_VALUE_TO, TRANSFER_ALL_AMOUNT)
        except Exception as e:
            logger.error(f'[{across.address}] error occured - {e}')
        time.sleep(random.randint(SLEEP_FROM, SLEEP_TO))

if __name__ == '__main__':
    main()
