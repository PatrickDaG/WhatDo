#!/usr/bin/env python3

import time

from rich.live import Live
from rich.console import Console
from rich.text import Text

from whatdo import util, steam, custom
from whatdo.interface import MainView
from whatdo.util import getch

import whatdo.state as state

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

def main():
    console = Console()

    def reroll():
        state.current_game = util.choose_random(list(current_games().values()))
    reroll()

    def quit():
        for i in all_games:
            i.save()
        exit(0)

    def exclude():
        state.current_game["exclude"] = True
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

    def add():
        return custom.add_custom()

    with Live(MainView(), screen = True, refresh_per_second = 12) as live:
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
            if inp == "a":
                live.stop()
                add()
                live.start()
