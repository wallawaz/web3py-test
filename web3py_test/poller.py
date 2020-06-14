import asyncio
from web3.auto import w3
from web3 import Web3
from .abi import ABI, UNISWAP_ABI
from .logger import LOGGER

class Poller:
    def __init__(self, contract_addresses, fromBlock="latest", abi=None):
        self.fromBlock = fromBlock
        self.abi = self._get_abi(abi)
        self.contracts = self._get_erc20s(contract_addresses)
        self.tasks = []
        self.abi = self._get_abi(abi)
    
    def _get_abi(self, abi):
        if abi is None:
            self.abi_type = "base"
            return ABI
        elif abi == "uniswap":
            self.abi_type = "uniswap"
            return UNISWAP_ABI
        else:
            raise Exception("invalid abi type")

    def _get_erc20s(self, contract_addresses):
        contracts = dict()
        for addr in contract_addresses:
            C = w3.eth.contract(Web3.toChecksumAddress(addr), abi=self.abi)
            name = C.functions.name().call()
            name = LOGGER.info(f"Polling: {name}")

            # if self.abi_type == "uniswap":
            #     exchange = C.functions.getEthToTokenOutputPrice(tokens_bought=str(1).encode().call()
            #     print(f"Exchange: {exchange}")

            # create the event_filter on the contract
            event_filter = C.events.Transfer.createFilter(fromBlock=self.fromBlock)
            contracts[name] = event_filter

        return contracts

    async def read_events_from_contract(self, event_filter, poll_interval=3):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            await asyncio.sleep(poll_interval)

    async def run(self):
        for contract in self.contracts.keys():
            self.tasks.append(
                await self.read_events_from_contract(self.contracts[contract])
            )
        asyncio.gather(*self.tasks)

    def handle_event(self, event):
        """Currently just printing"""
        LOGGER.info(f"EVENT: {event}")
