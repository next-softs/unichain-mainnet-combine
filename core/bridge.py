from concurrent.futures import ThreadPoolExecutor

from utils.logs import logger
from models.chains import Chains
from contracts.Bridge import *
from contracts.Uniswap import *
from config import *

import random, time

address_no_balance = []

def bridge(acc):
    bridges = {"gas.zip": GasZip, "superbridge": SuperBridge}

    amount = round(random.uniform(*BridgeSettings.amounts), random.randint(*GeneralSettings.precision))

    client = Uniswap(acc, Chains.Unichain)
    # if BridgeSettings.min_amount < float(client.balance()) + float(client.balance_weth()):
    #     logger.warning(f"{client.acc_name} на балансе больше {BridgeSettings.min_amount} ETH бриджить не будем")
    #     return True

    chains = {"base": Chains.Base, "op": Chains.OP}
    chains_list = BridgeSettings.chains
    random.shuffle(chains_list)

    client = None
    for chain in chains_list:
        client = bridges[random.choice(BridgeSettings.bridges)](acc, chains[chain])
        if client.balance() >= amount: break
    else:
        logger.warning(f"{client.acc_name} в указанных сетях нет нужного кол-ва ETH {amount}")
        address_no_balance.append(client.address)
        return False

    resp = client.bridge(amount)

    time.sleep(random.randint(*BridgeSettings.delay))
    return resp

def start_bridge(accounts):
    random.shuffle(accounts)

    with ThreadPoolExecutor(max_workers=GeneralSettings.threads) as executor:
        futures = [executor.submit(bridge, acc) for acc in accounts]

        for future in futures:
            future.result()