from web3 import Web3

class CoinInfo:
    def __init__(self, coin, address, decimals=18, abi=[]):
        w3 = Web3()

        self.coin = coin
        self.address = w3.to_checksum_address(address)
        self.decimals = decimals
        self.abi = abi

    def __repr__(self):
        return self.coin

class Coins:
    WETH = CoinInfo(coin="WETH", address="0x4200000000000000000000000000000000000006")
    ETH = CoinInfo(coin="ETH", address="0x0000000000000000000000000000000000000000")
    USDC = CoinInfo(coin="USDC", address="0x078D782b760474a361dDA0AF3839290b0EF57AD6", decimals=6)

    @classmethod
    def coins_list(self):
        resp = {}
        for name, obj in vars(self).items():
            if isinstance(obj, CoinInfo):
                resp[obj.coin] = obj

        return resp

