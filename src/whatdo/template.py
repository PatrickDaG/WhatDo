#!/usr/bin/env python3
"""
 File for additional game sources
 While primarily intended for games it can also be used for any number
 of other things for example tasks, todos or chores

 These kind of substitute for classes in that they each have their
 own json representation and values
 these have to include values for:
 "name"
 "appid"
 "type": the type of game, in most cases equal to the source or game launcher
 Additionally you can include
 "img_icon_url"
 "img_logo_url"
 As links to pictures
 -- Not yet implemented --

 This template lacks any function to add new entrys
 which is very dependend on what kind of game you implement
"""

from whatdo.util import load_games, save_games

cache = None
"""
Cached games for faster access
While not necessary usage is heavily encouraged to prevent ecessive load times
"""

name = "template"
""" Name of importer, to be able to include in menus """

file = name + ".json"
""" filename of save file, should end in .json """


def games() -> dict:
    """
    Return all currently available games

    Prints error to stderr on no games existing

    Returns
    -------
    dict
        dictionary from game uuid to json of game object
        None if failed to get any games
    """
    global cache
    if cache is not None:
        return cache
    try:
        cache = load_games(file)
    except FileNotFoundError:
        print("Save file not found")
        cache = {}
    return cache

def save():
    """
    Saves current games to disk
    """
    if cache is None:
        return
    save_games(cache, file)

