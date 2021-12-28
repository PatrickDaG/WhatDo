#!/usr/bin/env python3

import random
import json
# some util function to assist me

data_folder = "./data/"

def build_request(url: str, location: str, options: dict) -> str:
    req = url + location + "?"
    for key,value in options.items():
        req += key + "=" + value + "&"
    return req[0:-1]

def choose_random(choices):
            return random.choice([c for c in choices if
                not c.get("exclude", False)])

def col(color: str) -> str: # wen ich fancy sein will can hier auf color support getestet werden
    return color

def save_games(games: dict, filename: str):
    with open(data_folder + filename, "w") as f:
        json.dump(games, f)

def load_games(filename: str) -> dict:
    with open(data_folder + filename, "r") as f:
        return json.load(f)

from howlongtobeatpy import HowLongToBeat, HowLongToBeatEntry

def playtime(game_name: str) -> HowLongToBeatEntry:
    res = HowLongToBeat().search(game_name)
    if res is None or len(res) == 0:
        return None
    return(max(res, key=lambda element: element.similarity))
