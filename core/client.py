from models.coins import Coins

from config import *
from utils.file_manager import append_to_txt
from utils.logs import logger

from decimal import Decimal
import time, random


class Client:
    def __init__(self, account):
        self.coins = Coins()
        self.account = account

        logger.info(f"{self.account.private_key[:5]}..{self.account.private_key[-5:]} запуск бота..")

    def sleep(self, delay):
        s = random.randint(*delay)
        logger.info(f"{self.acc_name} ожидаем {s} сек..")
        time.sleep(s)

    def start(self):
        pass
