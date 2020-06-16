import csv
from datetime import datetime
import os
import time

WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
API_KEY = os.getenv("ETHERSCAN_KEY")

HEADERS = ["ts", "source", "blocknumber", "blockhash"]

def get_filename():
    fn = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if API_KEY is not None:
        return {"filename": f"{fn}_etherscan.csv", "provider_type": "etherscan"}

    provider_formats = {"file": "local_ipc", "ws": "infura_ws"}
    provider_type = WEB3_PROVIDER_URI.split(":")[0]
    return {
       "filename": f"{fn}_{provider_type}.csv",
       "provider_type": provider_type,
    }

def main_web3():
    from web3.auto import w3
    file_name_dict = get_filename()

    rows = []
    with open(file_name_dict["filename"], "w") as of:
        csvw = csv.DictWriter(of, fieldnames=HEADERS)
        csvw.writeheader()
        for i in range(1000):
            latest_block = w3.eth.getBlock("latest")
            rows.append({
              "ts":time.time_ns(),
              "source":file_name_dict["provider_type"],
              "blocknumber":latest_block.get("number"),
              "blockhash":latest_block.get("transactionsRoot").hex(),
            })
        csvw.writerows(rows)



# The Etherscan Ethereum Developer APIs are provided as a community service and
# without warranty, so please just use what you need and no more. We support
# both GET/POST requests and there is a rate limit of 5 calls per sec/IP.
def main_etherscan():
    import etherscan
    file_name_dict = get_filename()
    es = etherscan.Client(
    api_key=API_KEY,
    cache_expire_after=5,
    )
    rows = []
    with open(file_name_dict["filename"], "w") as of:
        csvw = csv.DictWriter(of, fieldnames=HEADERS)
        csvw.writeheader()
        for i in range(1000):
            blocknumber = es.get_block_number()
            blockhash = es.get_block_by_number(blocknumber).get("transactionsRoot")
            rows.append({
              "ts":time.time_ns(),
              "source":file_name_dict["provider_type"],
              "blocknumber":blocknumber,
              "blockhash":blockhash,
            })
            time.sleep(.215)
        csvw.writerows(rows)

def main():
    if WEB3_PROVIDER_URI is not None:
        main_web3()
    elif API_KEY is not None:
        main_etherscan()
    else:
        raise Exception("Env Vars not set: `WEB3_PROVIDER_URI` or `ETHERSCAN_KEY` must be set")

if __name__ == "__main__":
    main()

