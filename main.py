import random
import time

from loguru import logger

from config import ACCOUNTS
from modules.across import Across
from settings import CHAIN, AMOUNT_FROM, AMOUNT_TO, ALL_AMOUNT, KEEP_VALUE_FROM, KEEP_VALUE_TO


def main():
    random.shuffle(ACCOUNTS)
    for index, private_key in enumerate(ACCOUNTS):
        across = Across(private_key, index)
        try:
            across.deposit(CHAIN, AMOUNT_FROM, AMOUNT_TO, KEEP_VALUE_FROM, KEEP_VALUE_TO, ALL_AMOUNT)
        except Exception as e:
            logger.error(f'[{across.address}] error occured - {e}')
            time.sleep(random.randint(30, 60))


if __name__ == '__main__':
    main()
