#!/usr/bin/env python3

# File for additional game sources
# While primarily intended for games it can also be used for any number of other things
#
# These kind of represent classes in that they each have their own json representation
# These should include values for:
# "name"
# "appid"
# "type": the type of game, in most cases equal to the name of the file which handles it
# Additionally you can include
# "img_icon_url"
# "img_logo_url"
# As links tho pictures
# -- Not yet implemented --

# The games of this file should then be a dict from app id to the game itself

from whatdo.util import load_games, save_games

# cached games to prevent having to load/save games every single time
cache = None

# name of this type of game
# To be used in type and if asking for the name of this game importer
name = "template"

# file where json is to be saved/loaded from
# will be located in data folder
file = name + ".json"

# this function should return all currenly available games, without caring about excluded or other tags
# the usage of cache is not mandatory but heavily encouraged
def games() -> dict:
    global cache
    if cache is not None:
        return cache
    try:
        cache = load_games(file)
    except FileNotFoundError:
        print("Save file not found")
        cache = {}
    return cache

# function to save all games in json format to disk
def save():
    if cache is None:
        return
    save_games(cache, file)

# This template lacks any function to add new entrys
# This is very dependend on what kind of game you implement
# and should be done then
