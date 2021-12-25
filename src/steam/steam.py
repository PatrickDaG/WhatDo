#!/usr/bin/env python3

import requests
import json

from sys import stderr

from whatdo.util import build_request, load_games

def get_api_key(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read().strip()

def sync_games(offline_games: dict) -> dict:
    online_games = get_online_games()
    for k,v in online_games.items():
        o = offline_games.get(k)
        if o is not None:
            v["exclude"] = o.get("exclude", False)
    return online_games

def get_online_games() -> dict:
    address = "https://api.steampowered.com"
    method = "/IPlayerService/GetOwnedGames/v0001/"
    options = { "key": get_api_key(".api_key"), # should try not to publish this thx
            "steamid": "76561198060162001", # has to be 64 id, maybe add function to map from custom id to that
            "include_appinfo": "true"
            }
    req = build_request(address, method, options)
    arr = json.loads(requests.get(req).text)["response"]["games"]
    erg = {}
    for j in arr:
        erg[str(j["appid"])] = j
    return erg

def get_offline_games() -> dict:
    return load_games("steam.json")

def get_games() -> dict:
    try:
        erg = get_offline_games()
    except FileNotFoundError:
        print("No local file found, downloading from api", file=stderr)
        erg = get_online_games()
    return erg
