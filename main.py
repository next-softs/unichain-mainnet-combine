import random, time
import threading

from models.accounts import Accounts
from models.chains import Chains

from utils.first_message import first_message, get_action
from utils.logs import logger
from config import *

from core.bridge import start_bridge, address_no_balance
from core.info_wallets import start_info
from core.swap import start_swap, swap
from core.deploy import start_deploy
from core.nft import start_mint_nft


def main():
    accounts_manager = Accounts()
    accounts_manager.loads_accs()
    accounts = accounts_manager.accounts
    random.shuffle(accounts)

    action = get_action(["Запуск нескольких модулей", "Баланс ETH и кол-во транзакций", "Деплой контракта Owlto", "Минт NFT", "Бридж", "Свапы"])

    if action == "Запуск нескольких модулей":
        modules_start = {"bridge": start_bridge, "swap": start_swap, "mint_nft": start_mint_nft, "deploy": start_deploy}

        ths = []
        for m in GeneralSettings.start_modules:
            ths.append(threading.Thread(target=modules_start[m], args=(accounts.copy(),)))
            random.shuffle(accounts)

        for th in ths:
            th.start()

        for th in ths: th.join()

    elif action == "Баланс ETH и кол-во транзакций":
        start_info(accounts)

    elif action == "Бридж":
        start_bridge(accounts)

        print(f"\nНа этих кошельках не было ETH для бриджа:")
        for addr in address_no_balance:
            print(addr)

    elif action == "Свапы":
        start_swap(accounts)

    elif action == "Минт NFT":
        start_mint_nft(accounts)

    elif action == "Деплой контракта Owlto":
        start_deploy(accounts)

    else:
        logger.warning(f"Выбран вариант, которого нет!")

if __name__ == '__main__':
    first_message()
    main()


