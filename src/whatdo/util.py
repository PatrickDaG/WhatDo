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

def col(color: str) -> str: # wen ich fancy sein will can hier auf color support getestet werden
    """
    for color output in print

    Parameters
    ----------
    color
        Escape sequence for term color

    Returns
    -------
    str
        the same escape sequence if color is supported, else empty
        ----- NOT YET IMPLEMENTED -----
    """
    return color

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

from pyfiglet import Figlet
from rich.text import Text
from rich.console import Console, ConsoleOptions, RenderResult

class FigletText:
    """A renderable to generate figlet text that adapts to fit the container."""

    def __init__(self, text: str) -> None:
        self.text = text

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Build a Rich renderable to render the Figlet text."""
        size = min(options.max_width / 2, options.max_height)
        if size < 4:
            yield Text(self.text, style="bold")
        else:
            if size < 7:
                font_name = "mini"
            elif size < 8:
                font_name = "small"
            elif size < 10:
                font_name = "standard"
            else:
                font_name = "big"
            font = Figlet(font=font_name, width=options.max_width)
            yield Text(font.renderText(self.text).rstrip("\n"), style="bold")

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
