import json, os, functools
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

@functools.lru_cache(maxsize=1)
def load_stores() -> List[Dict]:
    with open(os.path.join(DATA_DIR, "stores.json"), "r", encoding="utf-8") as f:
        return json.load(f)

@functools.lru_cache(maxsize=1)
def load_prices() -> List[Dict]:
    with open(os.path.join(DATA_DIR, "prices.json"), "r", encoding="utf-8") as f:
        return json.load(f)
