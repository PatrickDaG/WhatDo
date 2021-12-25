#!/usr/bin/env python3

import json
import requests

def get_api_key(filename: str) -> str:
    f = open(filename, "r")
    return f.read().strip()

steam_addr = "https://api.steampowered.com"
steam_method = "/IPlayerService/GetOwnedGames/v0001/"
steam_option = { "key": get_api_key("api_key"),
        "steamid": "76561198060162001", # has to be 64 id, maybe add function to map from custom id to that
        "include_appinfo": "true"
        }

def build_request(url: str, location: str, options: dict) -> str:
    req = url + location + "?"
    for key,value in options.items():
        req += key + "=" + value + "&"
    return req[0:-1]

def main():
    erg = requests.get(build_request(steam_addr, steam_method, steam_option))
    j = json.loads(erg.text)
    print(erg.text)
