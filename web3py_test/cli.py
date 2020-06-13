from web3py_test import __version__
from web3py_test.poller import Poller
from web3py_test.historic import HistoricExchanges

import asyncio
import click

@click.command()
@click.version_option(version=__version__)
@click.option("--abi")
@click.option("--contracts", "-c", multiple=True)
def main(contracts, abi):
    poller = Poller(contracts, abi=abi)
    asyncio.run(poller.run())

@click.command()
@click.option("--factory-contract", required=True)
@click.option("--from-block", default="latest")
def main_historic(factory_contract, from_block):
    historic_ex = HistoricExchanges(factory_contract, from_block=from_block)
    historic_ex.run()
