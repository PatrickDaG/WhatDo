#!/usr/bin/env python3

import time

from rich.text import Text
from whatdo import util, steam, custom, interface
from whatdo.util import getch

all_games = [steam, custom]
"""
All game sources currently available
"""

current_games_choice = all_games
"""
Currentry selected choice
Must be subset of all_games
---- NOT YET IMPLEMENTED ----
"""

def current_games() -> dict:
    """
    joined dict of all game sources

    Returns
    -------
    dict
        dict from appid to game of all games
    """
    erg = {}
    for i in current_games_choice:
        erg.update(i.games())
    return erg

def list_current():
    """
    List all currently selected games on stdout

    Currently no ordering is guaranteed
    """
    for i in current_games().values():
        if not i.get("exclude", False):
            print(i["type"] + ": " + i["name"])

from rich.live import Live
from rich.console import Console

def main():
    cur = util.choose_random(list(current_games().values()))
    main_view = interface.MainView(cur)
    console = Console()

    def reroll():
        cur = util.choose_random(list(current_games().values()))
        main_view.game = cur

    def quit():
        for i in all_games:
            i.save()
        exit(0)

    def exclude():
        cur["exclude"] = True
        reroll()
    def sync():
        with console.status("Syncing") as status:
            if steam.sync_games():
                status.stop()
                console.rule("Success", style = "green")
                time.sleep(1)
            else:
                status.stop()
                console.rule("Failed", style = "red")
                time.sleep(1)
    def _list():
        gamelist = Text()
        for i in current_games().values():
            gamelist.append(Text.from_markup(f"[purple]{i['type']}:[/purple] {i['name']}"))
            if i.get('exclude'):
                gamelist.append(Text.from_markup(f"[red](excluded)[/red]"))
            gamelist.append("\n")
        with console.pager(styles = True):
            console.print(gamelist)


    with Live(main_view, screen = True, refresh_per_second = 12) as live:
        while True:
            inp = getch()
            if inp == "r":
                reroll()
            if inp == "q":
                quit()
            if inp == "e":
                exclude()
            if inp == "s":
                live.stop()
                sync()
                live.start()
            if inp == "l":
                live.stop()
                _list()
                live.start()
