from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
from eth_account.messages import encode_typed_data

from contracts.default import Default
from utils.encode import get_data_byte64
from utils.logs import logger

from models.chains import Chains
from models.coins import Coins
import time


class Uniswap(Default):
    def __init__(self, account, chain=Chains.Unichain):
        super().__init__(account.private_key, chain.rpc, [], "", account.proxy)
        self.api_key = ""

    @retry(stop=stop_after_attempt(1), wait=wait_fixed(3))
    def call_api(self, url, params):
        params["gasStrategies"] = [{"limitInflationFactor": 1.15,"displayLimitInflationFactor": 1.15,"priceInflationFactor": 1.5,"percentileThresholdFor1559Fee": 75,"minPriorityFeeGwei": 2,"maxPriorityFeeGwei": 9}]

        headers = self.session.headers
        headers["x-api-key"] = self.api_key

        resp = self.session.post(url, json=params, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"[{resp.status_code}] {resp.text} {url}")

        return resp.json()

    def get_api_key(self):
        resp = self.session.get("https://app.uniswap.org/static/js/main.5ff8e115.js")
        return resp.text.split('REACT_APP_TRADING_API_KEY:"')[1].split('"')[0]

    def get_quote(self, in_token, out_token, in_amount):
        params = {
            "amount": str(in_amount),
            "swapper": self.address,
            "tokenIn": in_token,
            "tokenInChainId": self.chain_id,
            "tokenOut": out_token,
            "tokenOutChainId": self.chain_id,
            "type": f"EXACT_INPUT",
            "urgency": "normal",
            "protocols": ["V4", "V3", "V2"],
            "slippageTolerance": 2.5
        }

        return self.call_api("https://trading-api-labs.interface.gateway.uniswap.org/v1/quote", params)

    def get_data(self, quote, permitData={}, signature=None):
        params = {
            "quote": quote,
            "simulateTransaction": True,
            "refreshGasPrice": True,
            "gasStrategies": [],
            "urgency": "normal",
            "refreshGasPrice": True
        }

        if permitData: params["permitData"] = permitData
        if signature: params["signature"] = signature

        return self.call_api("https://trading-api-labs.interface.gateway.uniswap.org/v1/swap", params)

    def sign(self, message):
        message_sign = {
            "types": message["types"],
            "domain": message["domain"],
            "primaryType": "PermitSingle",
            "message": message["values"]
        }

        signable_message = encode_typed_data(full_message=message_sign)
        signed = self.w3.eth.account.sign_message(signable_message=signable_message,private_key=self.private_key)
        signature = signed.signature.hex()

        return "0x" + signature

    def swap(self, in_token, out_token, in_amount):
        try:
            if in_token.coin == "ETH" and out_token.coin == "WETH":
                return self.wrap(in_amount)
            elif in_token.coin == "WETH" and out_token.coin == "ETH":
                return self.unwrap(in_amount)

            if in_token.coin == "ETH": in_token = Coins.WETH

            self.api_key = self.get_api_key()
            amount_wei = self.gwei_to_wei(in_amount, self.decimals(in_token.address))

            # token_for_token
            if in_token.coin not in ["ETH", "WETH"]:
                allowed = self.get_allowance(in_token.address, "0xEf740bf23aCaE26f6492B10de645D6B98dC8Eaf3")

                if allowed < in_amount:
                    self.approve(spender="0xEf740bf23aCaE26f6492B10de645D6B98dC8Eaf3", token_address=in_token.address)
                    time.sleep(3)

                quote_data = self.get_quote(in_token.address, out_token.address, amount_wei)

                quote = quote_data["quote"]
                permitData = quote_data["permitData"]

                sign = self.sign(permitData) if permitData else None
                data = self.get_data(quote, permitData, sign)["swap"]

            # eth_for_token
            else:
                quote = self.get_quote(Coins.ETH.address, out_token.address, amount_wei)["quote"]
                data = self.get_data(quote)["swap"]

            tx = {
                "chainId": data["chainId"],
                "data": data["data"],
                "from": self.address,
                "nonce": self.nonce(),
                "to": self.w3.to_checksum_address(data["to"]),
                "value": hex(int(data["value"], 16)),

            }

            if out_token.coin in ["ETH", "WETH"]: decimals = 0
            else: decimals = self.decimals(out_token.address)

            return self.send_transaction(tx, f"swap {in_amount} {in_token.coin} > {self.wei_to_gwei(quote['output']['amount'], decimals)} {out_token.coin} (Uniswap)")

        except RetryError as err:
            last_attempt = err.last_attempt
            if last_attempt.failed:
                logger.error(f"{self.acc_name} swap {last_attempt.exception()}")

        except Exception as err:
            logger.error(f"{self.acc_name} swap {err}")

        return False

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
