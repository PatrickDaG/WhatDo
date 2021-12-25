#!/usr/bin/env python3

from steam.steam import get_games, sync_games
from whatdo.util import get_random, col, save_games, playtime


def main():
    steam_games = get_games()
    while True:
        cur = get_random(list(steam_games.values()))
        time = playtime(cur["name"])
        print("Current Game is: " + col("\x1b[34m") + cur["name"] + col("\x1b[m"))
        print("(" + col("\x1b[32m") + "r" + col("\x1b[m") + ") to reroll," +
            "(" + col("\x1b[33m") + "e" + col("\x1b[m") + ") to exclude," +
            "(" + col("\x1b[31m") + "q" + col("\x1b[m") + ") to quit," +
            "(" + col("\x1b[35m") + "s" + col("\x1b[m") + ") to sync games with online")
        print("Playtime: " + col("\x1b[35m") + time.gameplay_main + col("\x1b[m") +
             " " + time.gameplay_main_unit)
        inp = input(">")
        if inp == "e":
            cur["exclude"] = True
        elif inp == "q":
            save_games(steam_games, "steam.json")
            exit(0)
        elif inp == "s":
            steam_games = sync_games(steam_games)
            print("Successfully synced")
