#!/usr/bin/env python3

import uuid
from sys import stderr

from whatdo.util import load_games, save_games

cache = None
""" see `template.cache` """

name = "custom"
""" see `template.name` """

file = name + ".json"
""" see `template.file` """

def games() -> dict:
    """ see `template.games` """
    global cache
    if cache is not None:
        return cache
    try:
        cache = load_games(file)
    except FileNotFoundError:
        print("No custom games exist yet, start by adding some", file = stderr)
        cache = {}
    return cache


def save():
    """ see `template.save` """
    if cache is None:
        return
    save_games(cache, file)

def add_custom():
    """
    Add a new custom game wich command line interface

    Modifies the cache
    """

    erg = {}
    erg["name"] = input("Please enter a name:")
    erg["type"] = "custom"
    erg["img_icon_url"] = input("You may enter a icon url for display purpose:")
    erg["img_logo_url"] = input("Additionally you can enter a logo url:")
    # Check if such a game already exists
    # subject to extension with fuzzy matching
    for i in games().values():
        if i["name"] == erg["name"]:
            print("There seems to already exist a game with that name!")
            print("Do you want to: "
                    + "o" + "verwrite, "
                    + "a" + "dd anyway or "
                    + "c" + "cancel?")
            inp = input(">")
            if inp == "o":
                erg["appid"] = i["appid"]
                games()[erg["appid"]] = erg
                return
            if inp == "c":
                return
            break
    # generate random uuid
    erg["appid"]= str(uuid.uuid4())
    games()[erg["appid"]] = erg
