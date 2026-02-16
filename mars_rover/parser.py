"""Command parser for converting user input to command objects."""

from pydantic import ValidationError

from mars_rover.commands import (
    Command,
    MoveCommand,
    LeftCommand,
    RightCommand,
    ReportCommand,
    PlaceCommand,
)
from mars_rover.models import Direction, PlaceArgs
from mars_rover.exceptions import InvalidCommandException
from mars_rover.messages import ErrorMessages


class CommandParser:
    """Parses user input into commands."""

    PLACE_PREFIX = "PLACE"

    _COMMANDS = {
        "MOVE": MoveCommand,
        "LEFT": LeftCommand,
        "RIGHT": RightCommand,
        "REPORT": ReportCommand,
    }

    def parse(self, user_input: str) -> Command:
        """Parse user input into a command.

        Args:
            user_input (str): User input

        Returns:
            Command object

        Raises:
            InvalidCommandException: If command is unknown or invalid
        """
        cmd = user_input.strip().upper()

        if cmd.startswith(self.PLACE_PREFIX):
            return self._parse_place(cmd)

        if cmd in self._COMMANDS:
            return self._COMMANDS[cmd]()

        raise InvalidCommandException(
            ErrorMessages.UNKNOWN_COMMAND.format(command=user_input)
        )

    def _parse_place(self, text: str) -> PlaceCommand:
        """Parse PLACE command arguments.

        Args:
            text (str): PLACE command text

        Returns:
            PlaceCommand object

        Raises:
            InvalidCommandException: If PLACE command is malformed
        """
        raw_args = text[len(self.PLACE_PREFIX) :].strip()  # noqa: E203. Removes PLACE.
        parts = [p.strip() for p in raw_args.split(",")]

        if len(parts) != 3:
            raise InvalidCommandException(ErrorMessages.PLACE_REQUIRES_ARGS)

        try:
            args = PlaceArgs(
                x=int(parts[0]),
                y=int(parts[1]),
                direction=Direction(parts[2]),
            )
        except (ValueError, ValidationError) as exc:
            raise InvalidCommandException(
                ErrorMessages.INVALID_PLACE_COMMAND.format(text=text)
            ) from exc

        return PlaceCommand(args)
