from web3.auto import w3
from web3 import Web3
from .abi import NEW_EXCHANGE_ABI
from .logger import logger


class HistoricExchanges:
    def __init__(self, factory_contract, from_block):
        self.factory_contract = Web3.toChecksumAddress(factory_contract)
        self.factory_contract = factory_contract
        self.from_block = from_block

    def run(self):
        contract = w3.eth.contract(self.factory_contract, abi=NEW_EXCHANGE_ABI)

        event_filter = contract.events.NewExchange.createFilter(fromBlock=self.from_block)
        for event in event_filter.get_all_entries():
            print(event)