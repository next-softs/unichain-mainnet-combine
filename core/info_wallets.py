from concurrent.futures import ThreadPoolExecutor

from utils.logs import logger
from models.chains import Chains
from contracts.Swap import *
from config import *


def info(acc):
    client = Uniswap(acc, Chains.Unichain)
    return {
        "address": client.address,
        "balance": round(float(client.balance()) + float(client.balance_weth()), 6),
        "tx_count": int(client.nonce(), 16)
    }

def start_info(accounts):
    with ThreadPoolExecutor(max_workers=GeneralSettings.threads) as executor:
        futures = [executor.submit(info, acc) for acc in accounts]

        for future in futures:
            resp = future.result()
            logger.info(f"{resp['address']}: {resp['balance']} ETH | {resp['tx_count']} transactions")


