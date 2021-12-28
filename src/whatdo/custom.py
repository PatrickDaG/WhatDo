#!/usr/bin/env python3

import uuid

from whatdo.util import load_games, save_games, col

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


def save():
    if cache is None:
        return
    save_games(cache, file)

def add_custom():
    erg = {}
    erg["name"] = input("Please enter a name:")
    erg["img_icon_url"] = input("You may enter a icon url for display purpose:")
    erg["img_logo_url"] = input("Additionally you can enter a logo url:")
    for i in games().values():
        if i["name"] == erg["name"]:
            print("There seems to already exist a game with that name!")
            print("Do you want to: "
                    + col("\x1b[31m") + "o" + col("\x1b[m") + "verwrite, "
                    + col("\x1b[31m") + "a" + col("\x1b[m") + "dd anyway or "
                    + col("\x1b[31m") + "c" + col("\x1b[m") + "cancel?")
            inp = input(">")
            if inp == "o":
                erg["appid"] = i["appid"]
                games()[erg["appid"]] = erg
                return
            if inp == "c":
                return
            break
    erg["appid"]= str(uuid.uuid4())
    games()[erg["appid"]] = erg
