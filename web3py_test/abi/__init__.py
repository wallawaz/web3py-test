import json
import os

def get_abi():
    _dir = os.path.dirname(__file__)
    path = os.path.join(
        _dir,
        "base.json"
    )
    with open(path, "r") as fp:
        return json.load(fp)

ABI = get_abi()
