from concurrent.futures import ThreadPoolExecutor

from utils.logs import logger
from contracts.Nft import *
from config import *

import random, time


accounts_nft_count = {}

def min_nft(acc, nfts, market_nft):
    try:
        if market_nft == "nfts2":
            client = MintNft(acc)
        elif market_nft == "morkie":
            client = MorkieNFT(acc)
        else:
            return

        random.shuffle(nfts)

        nft = {}
        for n in nfts:
            if not NftSettings.mint_different or client.get_balance_nft(n["address"]) == 0:
                nft = n
                break
        else:
            logger.warning(f"{client.acc_name} все доступные nft есть на кошельке")
            del accounts_nft_count[client.acc.name]

            return None

        resp = client.mint(nft)

        if resp:
            accounts_nft_count[client.acc.name]["amount"] -= 1
            if accounts_nft_count[client.acc.name]["amount"] == 0: del accounts_nft_count[client.acc.name]

        return resp
    except Exception as err:
        logger.error(err)

def start_mint_nft(accounts):
    random.shuffle(accounts)

    for market_nft in NftSettings.market_nft:
        if market_nft == "nfts2":
            nfts = MintNft.get_nfts()
        elif market_nft == "morkie":
            nfts = MorkieNFT.get_nfts()
        else:
            logger.error(f"{market_nft} нет такого маркета nft")
            continue

        lastupdate_nft_list = int(time.time())

        for acc in accounts:
            accounts_nft_count[acc.name] = {
                "account": acc,
                "amount": random.randint(*NftSettings.amounts)
            }

        accounts_timeout = {}
        for i, acc in enumerate(accounts):
            accounts_timeout[acc.name] = int(time.time() + random.randint(*GeneralSettings.delay_start) * (int(i / GeneralSettings.threads)))


        while accounts_nft_count:
            time.sleep(5)

            if time.time() - lastupdate_nft_list >= 3600:
                if market_nft == "nfts2":
                    nfts = MintNft.get_nfts()
                elif market_nft == "morkie":
                    nfts = MorkieNFT.get_nfts()

                lastupdate_nft_list = int(time.time())

            start_accounts = []
            for acc, timeout in accounts_timeout.copy().items():
                if acc not in accounts_nft_count:
                    del accounts_timeout[acc]
                    continue

                if time.time() >= timeout:
                    start_accounts.append(accounts_nft_count[acc]["account"])
                    accounts_timeout[acc] = int(time.time() + random.randint(*NftSettings.delay))

            if start_accounts:
                with ThreadPoolExecutor(max_workers=GeneralSettings.threads) as executor:
                    futures = [executor.submit(min_nft, acc, nfts.copy(), market_nft) for acc in start_accounts]

                    for future in futures:
                        future.result()

    logger.info(f"все nft были заминчены")
