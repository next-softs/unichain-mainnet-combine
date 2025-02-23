from web3 import Web3

class CoinInfo:
    def __init__(self, coin, address, abi=[]):
        w3 = Web3()

        self.coin = coin
        self.address = w3.to_checksum_address(address)
        self.abi = abi

class Coins:
    ETH = CoinInfo(coin="ETH", address="0x4200000000000000000000000000000000000006")
