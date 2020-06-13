import json
import os

def get_abi(filename):
    _dir = os.path.dirname(__file__)
    path = os.path.join(
        _dir,
        filename,
    )
    with open(path, "r") as fp:
        return json.load(fp)

ABI = get_abi('base.json')
UNISWAP_ABI = get_abi('uniswap_abi.json')
NEW_EXCHANGE_ABI = [
    {
        "name": "NewExchange",
        "inputs": [
            {"type": "address", "name": "token", "indexed": True},
            {"type": "address", "name": "exchange", "indexed": True}
        ],
        "anonymous": False,
        "type": "event"
    },
]