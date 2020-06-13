from timeit import default_timer
from web3.auto import w3
import os

PROVIDER = os.getenv("WEB3_PROVIDER_URI")

def main():
    start = default_timer()
    blocks = set()
    for i in range(len(1000)):
        blocks.add(w3.eth.getBlock("latest"))
    total_time = default_timer() - start

    blocks = sorted(list(blocks))

    print(f"Provider: {PROVIDER}")
    print(f"{len(blocks)} blocks: {blocks}")
    print(f"Total time: {total_time}")

if __name__ == "__main__":
    main()