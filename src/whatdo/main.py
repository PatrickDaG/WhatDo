#!/usr/bin/env python3

from sys import stderr

from whatdo import util, steam, custom
from whatdo.util import col, FigletText

from rich.text import Text

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


def print_gametime(name: str) -> Text:
    """
    Print average gametime on stdout

    Print errors on stderr if no game found

    Parameters
    ----------
    name
        game name to search for

    Returns
    -------
    Text
        rich.text object of pretty output game time
    """

    try:
        time = util.playtime(name)
        if time is None:
            return Text()
        return Text.from_markup(f"Time to beat: [yellow]{time.gameplay_main} {time.gameplay_main_unit}[/yellow] for Game: " +
            f"[green]{time.game_name}[/green]")
    except TypeError:
        return Text()

def print_extra(game: dict, gametime:bool = False) -> Text:
    """
    Print the extra game information

    Parameters
    ----------
    game
        the game information to print
    gametime
        whether or not to fetch the gametime

    Returns
    -------
    Text
        The renderable text object
    """
    str = f"[purple]name:[/purple]\t\t{game['name']}\n"
    str += f"[purple]appid:[/purple]\t\t{game['appid']}\n"

    g = game.get("playtime_forever")
    if g is not None:
        str += f"[purple]playtime:[/purple]\t{g} minutes\n"
    str += f"[purple]type[/purple]\t\t{game['type']}\n"
    erg = Text.from_markup(str)
    if gametime:
        erg.append(print_gametime(game["name"]))
    return erg


menu = ("(" + col("\x1b[32m") + "r" + col("\x1b[0m") + ") to reroll\n" +
        "(" + col("\x1b[33m") + "e" + col("\x1b[0m") + ") to exclude\n" +
        "(" + col("\x1b[31m") + "q" + col("\x1b[0m") + ") to quit\n" +
        "(" + col("\x1b[35m") + "s" + col("\x1b[0m") + ") to sync games with online\n" +
        "(" + col("\x1b[35m") + "a" + col("\x1b[0m") + ") to add custom games\n" +
        "(" + col("\x1b[35m") + "l" + col("\x1b[0m") + ") to list current games\n")
"""
The available keybinds
Should be rewritten for rich without ansi codes
"""

from textual.app import App
from textual.widgets import Static
from rich.panel import Panel
from rich.align import Align

import asyncio

class TUI(App):

    async def bind_keys(self) -> None:
        await self.bind("r", "reroll")
        await self.bind("e", "exclude")
        await self.bind("q", "quit")
        await self.bind("s", "sync")
        await self.bind("a", "add_custom")
        await self.bind("l", "list")

    async def on_mount(self) -> None:
        await self.bind_keys()

        self.taskreroll = None
        self.game_title = Static(Text())
        self.extra = Static(Text())

        await self.action_reroll()

        await self.view.dock(self.game_title, edge = "top", size = 20)

        layout_keys = Panel(Text.from_ansi(menu), title = "Keybinds", border_style = "blue")
        keys = Static(layout_keys, name = "Keybinds")

        await self.view.dock(keys, edge = "right", size = 50)

        await self.view.dock(self.extra, edge = "bottom")

    async def interuptible_reroll(self) -> None:
        self.current = util.choose_random(list(current_games().values()))

        await self.game_title.update(Align(FigletText(self.current["name"]), "center", vertical = "middle"))
        await self.extra.update(Panel(print_extra(self.current), title = "Game", border_style = "red"))
        self.refresh()
        await self.extra.update(Panel(print_extra(self.current, gametime = True), title = "Game", border_style = "green"))

    async def action_reroll(self) -> None:
        if self.taskreroll is not None:
            self.taskreroll.cancel()
        self.taskreroll = asyncio.ensure_future(self.interuptible_reroll())

    async def action_exclude(self) -> None:
        self.current["exclude"] = True
        await self.action_reroll()

    async def action_quit(self) -> None:
        for i in all_games:
            i.save()
        return await super().action_quit()

    async def action_sync(self) -> None:
        """
        Not fully working
        """
        await self.game_title.update(Text("Syncing ..."))
        if steam.sync_games():
            await self.game_title.update(Text("Successfully synced"))
        else:
            await self.game_title.update(Text("Could not sync correctly. Please confirm working connection as well as correct api key"))
            await self.action_quit()
        await self.action_reroll()


def tui():
    TUI.run()

