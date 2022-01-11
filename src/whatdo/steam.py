#!/usr/bin/env python3

from typing import Optional
import requests
import json

from sys import stderr

from whatdo.util import build_request, load_games, save_games

cache = None
""" see `template.cache` """

name = "steam"
""" see `template.name` """

file = name + ".json"
""" see `template.file` """

key_file = ".api_key"
"""
file in which steam api key is saved
DO NOT COMMIT
"""

def api_key(filename: str) -> str:
    """
    return api key as string

    Parameters
    ----------
    filename
        File relative to current directory from which to read key

    Returns
    -------
    str
        API key as string
    """

    with open(filename, 'r') as f:
        return f.read().strip()

def sync_games() -> bool:
    """
    Sync downloaded games with games from official api

    Returns
    -------
    bool
        Whether it succeeded in updating, does not tell if it actually changed anything
    """

    global cache
    online = online_games()
    offline = games()
    if online is None:
        return False
    if offline is None:
        return False
    for k,v in online.items():
        o = offline.get(k)
        if o is not None:
            v["exclude"] = o.get("exclude", False)
    cache = online
    return True

def online_games() -> Optional[dict]:
    """
    Fetch games from Steam API

    Returns
    -------
    dict
        dictionary from appid to json of game
        None if failed
    """
    address = "https://api.steampowered.com"
    method = "/IPlayerService/GetOwnedGames/v0001/"
    options = { "key": api_key(key_file),
            "steamid": "76561198060162001",
            # has to be 64 id, maybe add function to map from custom id to that
            # also should not be hardcoded
            "include_appinfo": "true"
            }
    # add try except if no internet connection exists
    req = build_request(address, method, options)
    try:
        arr = json.loads(requests.get(req).text)["response"]["games"]
    except requests.exceptions.ConnectionError:
        print("Could not get games, Maybe check your connection", file=stderr)
        return None
    erg = {}
    for j in arr:
        j["type"] = name
        erg[str(j["appid"])] = j
    return erg

def save():
    """ see `template.save` """
    if cache is None:
        return
    save_games(cache, file)

def games() -> Optional[dict]:
    """ see `template.games` """
    global cache
    if cache is not None:
        return cache
    try:
        cache = load_games(file)
        return cache
    except FileNotFoundError:
        print("No local file found, downloading from api", file=stderr)
    except json.decoder.JSONDecodeError:
        print("error parsing json, downloading from api", file = stderr)
    cache = online_games()
    return cache
