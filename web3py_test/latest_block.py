import os
from time import time_ns

from web3.auto import w3

PROVIDER = os.getenv("WEB3_PROVIDER_URI")

def main():
    for i in range(1000):
        latest_block = w3.eth.getBlock("latest").get("transactionsRoot")
        print(f"{time_ns()}: tx: {latest_block.hex()}")

if __name__ == "__main__":
    main()
