#!/usr/bin/env python3

from whatdo import util, steam
from whatdo.util import col


def main():
    while True:
        cur = util.choose_random(list(steam.games().values()))
        print("Current Game is: " + col("\x1b[34m") + cur["name"] + col("\x1b[m"))
        print("(" + col("\x1b[32m") + "r" + col("\x1b[m") + ") to reroll," +
            "(" + col("\x1b[33m") + "e" + col("\x1b[m") + ") to exclude," +
            "(" + col("\x1b[31m") + "q" + col("\x1b[m") + ") to quit," +
            "(" + col("\x1b[35m") + "s" + col("\x1b[m") + ") to sync games with online")
        # should fix this
        # print actual name to see if its even right game and enabel failsafe if not in howlongtobeat
        #time = util.playtime(cur["name"])
        #print("Playtime: " + col("\x1b[35m") + time.gameplay_main + col("\x1b[m") +
        #     " " + time.gameplay_main_unit)
        inp = input(">")
        if inp == "e":
            cur["exclude"] = True
        elif inp == "q":
            util.save_games(steam.games(), steam.file)
            exit(0)
        elif inp == "s":
            if steam.sync_games():
                print("Successfully synced")
            else:
                print("Could not sync correctly. Please confirm working connection as well as correct api key")
