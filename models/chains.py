
class Chain:
    def __init__(self, chain, rpc, bridge_address=None):
        self.chain = chain
        self.rpc = rpc
        self.bridge_address = bridge_address

class Chains:
    OP = Chain(chain="OP", rpc="https://optimism.llamarpc.com", bridge_address="0x6f26Bf09B1C792e3228e5467807a900A503c0281")
    Base = Chain(chain="Base", rpc="https://base.llamarpc.com", bridge_address="0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64")
    Unichain = Chain(chain="Unichain", rpc="https://mainnet.unichain.org")
