from web3py_test import __version__
from web3py_test.poller import Poller


import asyncio
import click

@click.command()
@click.version_option(version=__version__)
@click.option("--contracts", "-c", multiple=True)
def main(contracts):
    print('main')
    poller = Poller(contracts)
    asyncio.run(poller.run())