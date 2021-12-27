#!/usr/bin/env python3

import uuid

from whatdo.util import load_games

cache = None
file = "custom.json"

def games() -> dict:
    global cache
    if cache is not None:
        return cache
    try:
        cache = load_games(file)
    except FileNotFoundError:
        print("No custom games exist yet, start by adding some")
        cache = {}
    return cache


def add_custom():
    erg = {}
    erg["name"] = input("Please enter a name:")
    erg["img_icon_url"] = input("You may enter a icon url for display purpose:")
    erg["img_logo_url"] = input("Additionally you can enter a logo url:")
    erg["appid"]= str(uuid.uuid4())
    games()[erg["appid"]] = erg
