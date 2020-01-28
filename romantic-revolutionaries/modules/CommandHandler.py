"""Command Control Module."""

import re

from modules.navigation.navcont import Directions

from kivy.app import App


class Command:
    """Command class."""

    def __init__(self, method, hotkeys):
        """Init instance."""
        self.method = method
        self.hotkeys = hotkeys
        self.app = App.get_running_app()

    def __str__(self):
        """Conver to string."""
        return f"{self.hotkey}: {self.name}"


class Help(Command):
    """Get help."""

    def __init__(self):
        """Initialize instance."""
        super().__init__(method=None, hotkeys=["help", "?", "h"])

    def parse(self, text):
        """Parse the command."""
        self.app.add_text(
            """[color=00FFFF]Movement:[/color]
        [go/move/walk] [north/south/east/west] [distance]
        """
        )

        return True


class Move(Command):
    """Move it."""

    def __init__(self, nav_control):
        """Initialize instance."""
        super().__init__(
            method=nav_control.go,
            hotkeys=[
                "go",
                "move",
                "head",
                "walk",
                "run",
                "north",
                "east",
                "south",
                "west",
                "n",
                "e",
                "s",
                "w",
            ],
        )
        self.nav_control = nav_control
        self.directions = {
            "north": Directions.NORTH,
            "east": Directions.EAST,
            "south": Directions.SOUTH,
            "west": Directions.WEST,
            "n": Directions.NORTH,
            "e": Directions.EAST,
            "s": Directions.SOUTH,
            "w": Directions.WEST,
        }

    def parse(self, words):
        """Parse the command."""
        direction, distance = None, None
        match = re.match(rf'({"|".join(self.hotkeys)})?( )?([a-zA-Z]+)?( )?(\d+)?', " ".join(words))

        if match:
            if match.group(1) in list(self.directions.keys()):
                direction = self.directions[match.group(1)]
            elif match.group(3) in list(self.directions.keys()):
                direction = self.directions[match.group(3)]
            if match.group(5) is not None:
                distance = int(match.group(5))
            else:
                distance = 1

        self.method(direction, distance)
        return True


class Look(Command):
    """Look in a direction."""

    def __init__(self, view_control):
        """Initialize instance."""
        super().__init__(
            method=view_control.look,
            hotkeys=["look", "north", "east", "south", "west", "n", "e", "s", "w"],
        )
        self.view_control = view_control
        self.directions = {
            "north": Directions.NORTH,
            "east": Directions.EAST,
            "south": Directions.SOUTH,
            "west": Directions.WEST,
            "n": Directions.NORTH,
            "e": Directions.EAST,
            "s": Directions.SOUTH,
            "w": Directions.WEST,
        }

    def parse(self, words):
        """Parse the command."""
        # direction
        match = re.match(rf'({"|".join(self.hotkeys)})?( )?([a-zA-Z]+)?( )?(\d+)?', " ".join(words))

        if match:
            if match.group(1) in list(self.directions.keys()):
                direction = self.directions[match.group(1)]
            elif match.group(3) in list(self.directions.keys()):
                direction = self.directions[match.group(3)]

        self.method(direction)
        return True


class CommandHandler:
    """Handle commands."""

    def __init__(self, app, **kwargs):
        """Initialize instance."""
        self.callbacks = set()
        self.app = app
        self.nav_control = kwargs["nav_control"]
        self.view_control = kwargs["view_control"]

        self.commands = [Help(), Move(self.nav_control), Look(self.view_control)]

    def parse_command(self, text):
        """Parse the command."""
        if type(text) is not str:
            raise ValueError(f"Command is not a string: {text}")

        text = text.lower()
        words = text.split()

        valid_command = False
        try:
            for command in self.commands:
                if words[0] in command.hotkeys:
                    valid_command = command.parse(words)
                    if valid_command:
                        break

            if not valid_command:
                self.app.add_text(f"I don't know what you mean by [color=FF0000]{text}[/color].")
        except IndexError:
            pass
