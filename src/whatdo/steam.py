#!/usr/bin/env python3

import requests
import json

from sys import stderr

from whatdo.util import build_request, load_games

cache = None
file = "steam.json"
key_file = ".api_key"

def api_key(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read().strip()

def sync_games() -> bool:
    global cache
    online = online_games()
    offline = games()
    if online is None:
        return False
    for k,v in online_games.items():
        o = offline.get(k)
        if o is not None:
            v["exclude"] = o.get("exclude", False)
    cache = online
    return True

def online_games() -> dict:
    address = "https://api.steampowered.com"
    method = "/IPlayerService/GetOwnedGames/v0001/"
    options = { "key": api_key(key_file), # should try not to publish this thx
            "steamid": "76561198060162001", # has to be 64 id, maybe add function to map from custom id to that
            "include_appinfo": "true"
            }
    # add try except if no internet connection exists
    req = build_request(address, method, options)
    arr = json.loads(requests.get(req).text)["response"]["games"]
    erg = {}
    for j in arr:
        erg[str(j["appid"])] = j
    return erg

def offline_games() -> dict:
    return load_games(file)

def games() -> dict:
    global cache
    if cache is not None:
        return cache
    try:
        cache = offline_games()
        # add another except if file is unparsable
    except FileNotFoundError:
        print("No local file found, downloading from api", file=stderr)
        cache = online_games()
    return cache
