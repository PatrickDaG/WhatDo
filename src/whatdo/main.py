#!/usr/bin/env python3

from asyncio.futures import Future
from sys import stderr

from textual.reactive import Reactive

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

    time = util.playtime(name)
    try:
        if time is None or int(time.gameplay_main) < 0:
            return Text()
    except TypeError:
        return Text()
    except ValueError:
        pass
    return Text.from_markup(f"Time to beat: [yellow]{time.gameplay_main} {time.gameplay_main_unit}[/yellow] for Game: " +
        f"[green]{time.game_name}[/green]")

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
from textual.widgets import ScrollView

from textual.widgets import Placeholder

import asyncio

class TUI(App):

    current = Reactive({})
    """
    Unused Should use this to automatically rerender the views on game change
    """

    async def bind_keys(self) -> None:
        await self.bind("r", "reroll")
        await self.bind("e", "exclude")
        await self.bind("q", "quit")
        await self.bind("s", "sync")
        await self.bind("a", "add_custom")
        await self.bind("l", "list")

    async def on_load(self) -> None:
        await self.bind_keys()

    async def on_mount(self) -> None:

        self.taskreroll = Future()
        self.game_title = Static(Text())
        self.extra = Static(Text())

        await self.action_reroll()

        await self.view.dock(self.game_title, edge = "top", size = 20)

        layout_keys = Panel(Text.from_ansi(menu), title = "Keybinds", border_style = "blue")
        keys = Static(layout_keys, name = "Keybinds")

        await self.view.dock(keys, edge = "right", size = 40)

        await self.view.dock(self.extra, edge = "bottom")

    async def interuptible_reroll(self) -> None:
        self.current = util.choose_random(list(current_games().values()))

        await self.game_title.update(Align(FigletText(self.current["name"]), "left", vertical = "middle"))
        await self.extra.update(Panel(print_extra(self.current), title = "Game", border_style = "red"))
        self.refresh()
        await self.extra.update(Panel(print_extra(self.current, gametime = True), title = "Game", border_style = "green"))

    async def action_reroll(self) -> None:
        if not self.taskreroll.done():
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
            lol = Static(Align(Panel(Text("Sync successfull!!"), width = 100, height = 3, border_style = "green"), align = "center", vertical = "middle"))
            await self.view.dock(lol, z= 1)
        else:
            await self.view.dock(Static(Align(Panel(Text("Could not sync correctly"), width = 100, height = 3, border_style = "red"), align = "center", vertical = "middle")), z = 1)
        self.view.widgets.remove(lol)

    async def action_list(self) -> None:
        """
        Renders scrollable popup with List of all games
        """
        gamelist = Text()
        for i in current_games().values():
            gamelist.append(Text.from_markup(f"[purple]{i['type']}:[/purple] {i['name']}"))
            if i.get('exclude'):
                gamelist.append(Text.from_markup(f"[red](excluded)[/red]"))
            gamelist.append("\n")
        view = ScrollView(gamelist, auto_width = False, gutter = 5)
        await self.view.dock(view, edge = "top", z = 1)

def tui():
    TUI.run()

