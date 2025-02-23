import random, time

from contracts.default import Default
from utils.encode import get_data_byte64

from decimal import Decimal
from models.coins import Coins


class Uniswap(Default):
    def __init__(self, account, chain):
        super().__init__(account.private_key, chain.rpc, [], "0xEf740bf23aCaE26f6492B10de645D6B98dC8Eaf3", account.proxy)

    def wrap(self, amount):
        data = get_data_byte64("0xd0e30db0")

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": "0x4200000000000000000000000000000000000006",
            "value": hex(self.gwei_to_wei(amount))
        }

        return self.send_transaction(tx, f"wrap ETH > WETH ({amount} ETH)")

    def unwrap(self, amount=0):
        if amount == 0:
            amount = self.token_balance("0x4200000000000000000000000000000000000006")

        data = get_data_byte64("0x2e1a7d4d", hex(self.gwei_to_wei(amount)))

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": "0x4200000000000000000000000000000000000006"
        }

        return self.send_transaction(tx, f"unwrap WETH > ETH ({amount} ETH)")

    def balance_weth(self):
        return float(self.token_balance("0x4200000000000000000000000000000000000006"))