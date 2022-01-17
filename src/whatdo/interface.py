"""
Interface classes and methods
"""

from pyfiglet import Figlet
from rich.text import Text
from rich.console import Console, ConsoleOptions, RenderResult
from rich.layout import Layout
from rich.panel import Panel

from whatdo import util
import whatdo.state as state

class FigletText:
    """A renderable to generate figlet text that adapts to fit the container."""

    def __init__(self, text: str, justify: str = "center") -> None:
        self.text = text
        self.justify = justify

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
            font = Figlet(font=font_name, width=options.max_width, justify = self.justify)
            yield Text(font.renderText(self.text), style="bold")

menu = Panel(Text.from_markup(
    """
    ([green]r[/green]) to reroll\n
    ([yellow]e[/yellow]) to exclude\n
    ([red]q[/red]) to quit\n
    ([magenta]s[/magenta]) to sync games\n
    ([magenta]a[/magenta]) to add a custom game\n
    ([magenta]l[/magenta]) to list available games\n
    """),
    title = "keybinds", border_style = "blue")

"""
The available keybinds
Should be rewritten for rich without ansi codes
"""
class GameInfo:

    def __rich_console__(
            self, console: Console, options: ConsoleOptions
    ) ->RenderResult:
        str = f"[purple]name:[/purple]\t\t{state.current_game['name']}\n"
        str += f"[purple]appid:[/purple]\t\t{state.current_game['appid']}\n"

        g = state.current_game.get("playtime_forever")
        if g is not None:
            str += f"[purple]playtime:[/purple]\t{g} minutes\n"
        str += f"[purple]type[/purple]\t\t{state.current_game['type']}\n"
        erg = Text.from_markup(str)
        erg.append(self.print_gametime())
        erg = Panel(erg, title = "Game", border_style = "green")
        yield erg

    def print_gametime(self) -> Text:
        time = util.playtime(state.current_game["name"])
        try:
            if time is None or int(time.gameplay_main) < 0:
                return Text()
        except TypeError:
            return Text()
        except ValueError:
            pass
        return Text.from_markup(f"Time to beat: [yellow]{time.gameplay_main} {time.gameplay_main_unit}[/yellow] for Game: " +
            f"[green]{time.game_name}[/green]")


class MainView:

    def __init__(self):
        self.title = FigletText("")
        self.game_info = GameInfo()

    def __rich_console__(
            self, console: Console, options: ConsoleOptions
    ) ->RenderResult:
        self.title.text = state.current_game["name"]
        erg = Layout()
        erg.split_column(
                Layout(self.title, name = "title", minimum_size = 8),
                Layout(name = "lower")
                )
        erg["lower"].split_row(
                Layout(self.game_info, name = "game_info"),
                Layout(menu, name = "menu", size = 40)
                )
        yield erg
