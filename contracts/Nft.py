import requests, web3, json

from contracts.default import Default
from utils.encode import get_data_byte64

from decimal import Decimal
from models.coins import Coins
from models.chains import Chains
from utils.session import headers
from config import NftSettings

from bs4 import BeautifulSoup as bs


class MintNft(Default):
    def __init__(self, account):
        super().__init__(account.private_key, Chains.Unichain.rpc, [], "0x00000000009a1E02f00E280dcfA4C81c55724212", account.proxy)
        self.acc = account

    @staticmethod
    def get_nfts():
        resp = requests.get("https://nfts2.me/unichain/top-minted/all-time", headers=headers(), timeout=10).text
        soup = bs(resp, "html.parser")
        data = json.loads(soup.find("script", id="__NEXT_DATA__").text)
        
        nfts = []
        for r in data["props"]["pageProps"]["data"]:
            if r["chainName"] == "unichain" and not r["soldout"] and int(r["mintFee"]) <= NftSettings.max_price * (10 ** 18) and NftSettings.min_nfts_minted < int(r["nftsMinted"]):
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

class MorkieNFT(Default):
    def __init__(self, account):
        super().__init__(account.private_key, Chains.Unichain.rpc, [], "", account.proxy)
        self.acc = account

    @staticmethod
    def get_nfts():
        resp = requests.get("https://morkie.xyz/")
        soup = bs(resp.text, "html.parser")

        nft_urls = []
        items = soup.find_all("article")
        for item in items:
            a = item.find("a")
            img = item.find_all("img")

            if a and img and "uni.svg" in img[-1].get("src"):
                nft_urls.append("https://morkie.xyz" + a.get("href"))

        nfts = []
        for nft_url in nft_urls:
            resp = requests.get(nft_url)
            soup = bs(resp.text, "html.parser")

            nft_name = soup.find("h4").text

            amount = soup.find("h2").text.split()[0]
            if amount.lower() == "free":
                amount = 0

            nfts.append({
                "title": nft_name,
                "address": soup.find_all("article")[1].find("span").text,
                "value": float(amount)
            })

        return nfts

    def mint(self, nft):
        data = data = get_data_byte64("0x84bb1e42", self.address, 1, "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", hex(self.gwei_to_wei(nft["value"])),
                                      hex(192), 160, 80, "", "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "", "", "")

        tx = {
            "chainId": self.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": nft["address"],
            "value": hex(self.gwei_to_wei(nft["value"]))
        }

        return self.send_transaction(tx, f"mint {nft['title']}")

    def get_balance_nft(self, address):
        return self.gwei_to_wei(self.token_balance(address))

