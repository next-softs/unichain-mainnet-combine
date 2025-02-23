import random
from concurrent.futures import ThreadPoolExecutor

import time

from config import *
from contracts.Swap import *
from utils.logs import logger
from models.chains import Chains


def wrap_unwrap(acc):
    try:
        client = Uniswap(acc, Chains.Unichain)

        amount = round(random.uniform(*WrapUnwrapSettings.amounts), random.randint(*GeneralSettings.precision))

        balance_eth = float(client.balance()) - 0.0005
        balance_eth = balance_eth if balance_eth > 0 else 0

        if balance_eth == 0:
            logger.warring(f"{client.acc_name} 0 ETH на балансе")
            return

        balance_weth = round(float(client.balance_weth()) * 0.99, 6)

        if amount > balance_eth and balance_weth != 0:
            client.unwrap(balance_weth)
        else:
            action = random.choice(["wrap", "unwrap"])
            if action == "wrap" or balance_weth == 0:
                amount = amount if amount < balance_eth else balance_weth
                client.wrap(amount)
            else:
                amount = amount if amount < balance_weth else balance_weth
                client.unwrap(amount)

    except Exception as err:
        logger.error(f"{client.acc_name} {err}")

def start_wrap_unwrap(accounts):
    random.shuffle(accounts)

    accs = {}
    for acc in accounts: accs[acc.name] = acc

    accounts_timeout = {}
    for i, acc in enumerate(accounts):
        accounts_timeout[acc.name] = int(time.time() + random.randint(*GeneralSettings.delay_start) * (int(i / GeneralSettings.threads)))

    while True:
        time.sleep(5)

        start_accounts = []
        for acc, timeout in accounts_timeout.copy().items():
            if time.time() >= timeout:
                start_accounts.append(accs[acc])
                accounts_timeout[acc] = int(time.time() + random.randint(*WrapUnwrapSettings.delay))

        if start_accounts:
            with ThreadPoolExecutor(max_workers=GeneralSettings.threads) as executor:
                futures = [executor.submit(wrap_unwrap, acc) for acc in start_accounts]

                for future in futures:
                    future.result()

