import random
from concurrent.futures import ThreadPoolExecutor

import time

from config import *
from contracts.Uniswap import *
from utils.logs import logger
from models.chains import Chains
from models.coins import Coins


def start_swap(accounts):
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
                accounts_timeout[acc] = int(time.time() + random.randint(*SwapSettings.delay))

        if start_accounts:
            with ThreadPoolExecutor(max_workers=GeneralSettings.threads) as executor:
                futures = [executor.submit(swap, acc) for acc in start_accounts]

                for future in futures:
                    future.result()

def sell_all(acc):
    client = Uniswap(acc)

    swaped = False
    for coin in SwapSettings.coins:
        coin = Coins().coins_list()[coin]
        balance_token = client.token_balance(coin.address)
        if balance_token > 0:
            client.swap(coin, Coins.ETH, balance_token)
            swaped = True
            time.sleep(5)

    return swaped

def swap(acc):
    try:
        client = Uniswap(acc)

        for i in range(random.randint(*SwapSettings.count_swap)):
            balance_eth = float(client.balance()) - 0.0002
            balance_eth = balance_eth if balance_eth > 0 else 0

            amount = round(random.uniform(*SwapSettings.amounts), random.randint(*GeneralSettings.precision))

            if balance_eth == 0 or balance_eth - amount < SwapSettings.min_amount_for_sell:
                logger.warning(f"{client.acc_name} слишком мало ETH на балансе, пытаемся все продать..")
                sell_all(acc)
                return True

            side = random.choice(["buy", "sell"])

            selled = False
            if side == "sell":
                selled = sell_all(acc)

            if side == "buy" or not selled:
                client.swap(in_token=Coins.ETH, out_token=Coins().coins_list()[random.choice(SwapSettings.coins)], in_amount=amount)

            client.sleep(SwapSettings.delay_swap)

    except Exception as err:
        logger.error(err)
