import random, time
import threading

from models.accounts import Accounts
from models.chains import Chains

from utils.first_message import first_message
from utils.logs import logger
from config import *

from core.bridge import start_bridge, address_no_balance
from core.info_wallets import start_info
from core.swap import start_wrap_unwrap
from core.deploy import start_deploy
from core.nft import start_mint_nft


def main():
    accounts_manager = Accounts()
    accounts_manager.loads_accs()
    accounts = accounts_manager.accounts
    random.shuffle(accounts)

    action = input("> 1. Запуск нескольких модулей\n"
                   "> 2. Баланс ETH и кол-во транзакций\n"
                   "> 3. Бридж\n"
                   "> 4. Warp Unwrap ETH\n"
                   "> 5. Минт рандомных NFT\n"
                   "> 6. Деплой контракта Owlto\n"
                   ">> ")
    print("-"*50+"\n")

    if action == "1":
        modules_start = {"bridge": start_bridge, "wrap_unwrap": start_wrap_unwrap, "mint_nft": start_mint_nft, "deploy": start_deploy}

        ths = []
        for m in GeneralSettings.start_modules:
            ths.append(threading.Thread(target=modules_start[m], args=(accounts.copy(),)))
            random.shuffle(accounts)

        for th in ths:
            th.start()

        for th in ths: th.join()

    elif action == "2":
        start_info(accounts)

    elif action == "3":
        start_bridge(accounts)

        print(f"\nНа этих кошельках не было ETH для бриджа:")
        for addr in address_no_balance:
            print(addr)

    elif action == "4":
        start_wrap_unwrap(accounts)

    elif action == "5":
        start_mint_nft(accounts)

    elif action == "6":
        start_deploy(accounts)

    else:
        logger.warning(f"Выбран вариант, которого нет!")

if __name__ == '__main__':
    first_message()
    main()


