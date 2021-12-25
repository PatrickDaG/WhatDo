#!/usr/bin/env python3

import requests
import json

from whatdo.util import build_request

def get_api_key(filename: str) -> str:
    f = open(filename, "r")
    return f.read().strip()

def get_games() -> json:
    address = "https://api.steampowered.com"
    method = "/IPlayerService/GetOwnedGames/v0001/"
    options = { "key": get_api_key(".api_key"), # should try not to publish this thx
            "steamid": "76561198060162001", # has to be 64 id, maybe add function to map from custom id to that
            "include_appinfo": "true"
            }
    req = build_request(address, method, options)
    return json.loads(requests.get(req).text)
