import asyncio
import logging
from web3.auto import w3
from web3 import Web3
from .abi import ABI

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()

class Poller:
    def __init__(self, contract_addresses, fromBlock="latest"):
        self.fromBlock = fromBlock
        self.contracts = self._get_erc20s(contract_addresses)
        self.tasks = []

    def _get_erc20s(self, contract_addresses):
        contracts = dict()
        for addr in contract_addresses:
            C = w3.eth.contract(Web3.toChecksumAddress(addr), abi=ABI)
            name = C.functions.name().call()
            name = logger.info(f"Polling: f{name}")

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
        asyncio.gather(**self.tasks) 

    def handle_event(self, event):
        """Currently just printing"""
        logger.info(f"EVENT: {event}")
