import os
import time

WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
API_KEY = os.getenv("ETHERSCAN_KEY")

def main_web3():
    from web3.auto import w3
    print(f"WEB3: {WEB3_PROVIDER_URI}")
    for i in range(1000):
        latest_block = w3.eth.getBlock("latest").get("transactionsRoot")
        print(f"{time.time_ns()}: tx: {latest_block.hex()}")


# The Etherscan Ethereum Developer APIs are provided as a community service and
# without warranty, so please just use what you need and no more. We support
# both GET/POST requests and there is a rate limit of 5 calls per sec/IP.
def main_etherscan():
    import etherscan
    print("ETHERSCAN")
    es = etherscan.Client(
    api_key=API_KEY,
    cache_expire_after=5,
    )
    calls = 0
    for i in range(1000):
        block = es.get_block_number()
        print(f"{time.time_ns()}: {block}")
        calls += 1
        if calls == 5:
            time.sleep(5)
            calls = 0

def main():
    if WEB3_PROVIDER_URI is not None:
        main_web3()
    elif API_KEY is not None:
        main_etherscan()
    else:
        raise Exception("Env Vars not set: `WEB3_PROVIDER_URI` or `ETHERSCAN_KEY` must be set")

if __name__ == "__main__":
    main()


