import requests, web3

from contracts.default import Default
from utils.encode import get_data_byte64

from decimal import Decimal
from models.coins import Coins
from models.chains import Chains
from utils.session import headers
from config import NftSettings


class MintNft(Default):
    def __init__(self, account):
        super().__init__(account.private_key, Chains.Unichain.rpc, [], "0x00000000009a1E02f00E280dcfA4C81c55724212", account.proxy)
        self.acc = account

    @staticmethod
    def get_nfts():
        resp = requests.get("https://nfts2.me/_next/data/b6zX-RsS2TNLvohfE1Tgz/unichain/free/all-time.json?params=unichain&params=free&params=all-time", headers=headers(), timeout=10).json()

        nfts = []
        for r in resp["pageProps"]["data"]:
            if r["chainName"] == "unichain" and not r["soldout"] and int(r["mintFee"]) <= NftSettings.max_price*(10**18) and NftSettings.min_nfts_minted < int(r["nftsMinted"]):
                nfts.append({
                    "title": r["name"].split(";")[0],
                    "address": web3.Web3().to_checksum_address(r["id"]),
                    "value": int(r["mintFee"]),
                    "nftsMinted": int(r["nftsMinted"])
                })

        return nfts

    def mint(self, nft, amount=1):
        data = get_data_byte64("0xb510391f", nft["address"], 40, 44,
                               f"449a52f8000000000000000000000000{self.address}000000000000000000000000000000000000000000000000000000000000000{amount}00000000000000000000000000000000000000000000000000000000")

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": self.contract_address,
            "value": hex(int(nft["value"]*1.1))
        }

        return self.send_transaction(tx, f"mint {nft['title']}")

    def get_balance_nft(self, address):
        return self.gwei_to_wei(self.token_balance(address))

