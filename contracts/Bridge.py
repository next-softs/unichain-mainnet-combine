import random, time

from contracts.default import Default
from utils.encode import get_data_byte64

from decimal import Decimal
from models.coins import Coins


class SuperBridge(Default):
    def __init__(self, account, chain):
        super().__init__(account.private_key, chain.rpc, [], chain.bridge_address, account.proxy)
        self.chain = chain

    def bridge(self, amount):
        in_amount = hex(self.gwei_to_wei(amount))
        out_amount = hex(self.gwei_to_wei(amount*random.uniform(0.98, 0.99)))

        start_time = int(time.time())
        fillDeadline = int(start_time + 14270)
        quoteTimestamp = int(start_time - 450)

        data = get_data_byte64("0x7b939232",
                               self.address, self.address,
                               Coins.ETH.address, Coins.ETH.address,
                               in_amount, out_amount, hex(130),
                               "0x0000000000000000000000000000000000000000",
                               hex(quoteTimestamp), hex(fillDeadline),
                               hex(0), hex(384), hex(0)) + "1dc0de0001"

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": self.contract_address,
            "value": hex(self.gwei_to_wei(amount))
        }

        return self.send_transaction(tx, f"bridge {self.chain.chain} > unichain ({amount} ETH)")
