#!/usr/bin/env python3

from sys import stderr

from whatdo import util, steam, custom
from whatdo.util import col

all_games = [steam, custom]

current_games_choice = all_games

def current_games() -> dict:
    erg = {}
    for i in current_games_choice:
        erg.update(i.games())
    return erg

def list_current():
    for i in current_games().values():
        print(i["type"] + ": " + i["name"])


def print_gametime(name: str):
    try:
        time = util.playtime(name)
        if time is None:
            print("No corresponding game found!", file = stderr)
            return
        print("Playtime: " + col("\x1b[35m") + time.gameplay_main + col("\x1b[m") +
            " " + time.gameplay_main_unit + " for Game: "
            + col("\x1b[33m")+ time.game_name + col("\x1b[m"))
    except TypeError:
        print("No Gametime found", file = stderr)


def main():
    while True:
        cur = util.choose_random(list(current_games().values()))
        print("Current Game is: " + col("\x1b[34m") + cur["name"] + col("\x1b[m"))
        print("(" + col("\x1b[32m") + "r" + col("\x1b[m") + ") to reroll, " +
            "(" + col("\x1b[33m") + "e" + col("\x1b[m") + ") to exclude, " +
            "(" + col("\x1b[31m") + "q" + col("\x1b[m") + ") to quit, " +
            "(" + col("\x1b[35m") + "s" + col("\x1b[m") + ") to sync games with online, " +
            "(" + col("\x1b[35m") + "a" + col("\x1b[m") + ") to add custom games, " +
            "(" + col("\x1b[35m") + "l" + col("\x1b[m") + ") to list current games")
        print_gametime(cur["name"])
        inp = input(">")
        if inp == "e":
            cur["exclude"] = True
        elif inp == "q":
            for i in all_games:
                i.save()
            exit(0)
        elif inp == "s":
            if steam.sync_games():
                print("Successfully synced")
            else:
                print("Could not sync correctly. Please confirm working connection as well as correct api key")
        elif inp == "a":
            custom.add_custom()
        elif inp == "l":
            list_current()
