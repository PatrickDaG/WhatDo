#!/usr/bin/env python3

import os
import random
import json
import sys
from typing import Optional
# some util function to assist me

data_folder = "./data/"
""" foldes in which to save all game jsons """

def build_request(url: str, location: str, options: dict) -> str:
    """
    build api http request

    Parameters
    ----------
    url
        url from which to get api
    location
        api location, most likely equal to api request
    options
        option like keys or users

    Returns
    -------
    str
        return string url of complete request
    """
    req = url + location + "?"
    for key,value in options.items():
        req += key + "=" + value + "&"
    # Do not return last & character
    return req[0:-1]

def choose_random(choices: list[dict]) -> dict:
    """
    Return random object from choices

    Parameters
    ----------
    choices
        List of choices

    Returns
    -------
    dict
        randomly selected entry
    """
    return random.choice([c for c in choices if
        not c.get("exclude", False)])

def save_games(games: dict, filename: str):
    """
    Save games to file

    Parameters
    ----------
    games
        dict of games to save
    filename
        filename to save to, will be relative to data_folder
    """
    with open(data_folder + filename, "w") as f:
        json.dump(games, f)

def load_games(filename: str) -> dict:
    """
    Load games from file
    Parameters
    ----------
    filename
        filename to load from, will be relative to data_folder

    Returns
    -------
    dict
        parsed json data from file
    """

    with open(data_folder + filename, "r") as f:
        return json.load(f)

def getch():
    """
    get single character unbuffered
    """
    import termios
    import sys, tty
    def linux_getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return linux_getch()

"""
This part is to get average playtime from HowLongToBeat
"""
from howlongtobeatpy import HowLongToBeat, HowLongToBeatEntry
from fake_useragent.errors import FakeUserAgentError

from sys import stderr

def playtime(game_name: str) -> Optional[HowLongToBeatEntry]:
    """
    Get average playtime from HowLongToBeat

    Parameters
    ----------
    game_name
        Name to search for in database

    Returns
    -------
    HowLongToBeatEntry
        Custom class to hold information about the gametime
    """

    try:
        # shitty library just print shit to stderr without actually
        # throwing exception
        old = stderr
        with open(os.devnull, "w") as f:
            sys.stderr = f
            res = HowLongToBeat().search(game_name)
        sys.stderr = old
    except FakeUserAgentError:
        print("error getting Fake User Agent for request", file=stderr)
        return None
    if res is None or len(res) == 0:
        # no game found
        return None
    return(max(res, key=lambda element: element.similarity))
