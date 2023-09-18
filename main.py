import random
import time

from loguru import logger

from config import ACCOUNTS
from modules.across import Across
from settings import CHAIN, AMOUNT_FROM, AMOUNT_TO, ALL_AMOUNT, KEEP_VALUE_FROM, KEEP_VALUE_TO


def main():
    print(f'\n{" " * 32}AUTHOR - https://t.me/CodeCashMafia{" " * 32}\n')
    print(f'\n{" " * 32}donate - EVM 0x98F93AD29d4Fe210b9D33E910335C88C333db87A{" " * 32}\n')

    random.shuffle(ACCOUNTS)
    for index, private_key in enumerate(ACCOUNTS):
        across = Across(private_key, index)
        try:
            across.deposit(CHAIN, AMOUNT_FROM, AMOUNT_TO, KEEP_VALUE_FROM, KEEP_VALUE_TO, ALL_AMOUNT)
        except Exception as e:
            logger.error(f'[{across.address}] error occured - {e}')
            time.sleep(random.randint(30, 60))

    print(f'\n{" " * 32}AUTHOR - https://t.me/CodeCashMafia{" " * 32}\n')
    print(f'\n{" " * 32}donate - EVM 0x98F93AD29d4Fe210b9D33E910335C88C333db87A{" " * 32}\n')

if __name__ == '__main__':
    main()
