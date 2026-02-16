"""CLI interface for Mars Rover Simulator."""

import sys
from typing import TextIO

from mars_rover.models import TableBounds
from mars_rover.rover import Rover
from mars_rover.parser import CommandParser
from mars_rover.exceptions import RoverException
from mars_rover.result import CommandResult


def run_cli_loop(
    parser: CommandParser, rover: Rover, in_stream: TextIO, out_stream: TextIO
) -> None:
    """Run interactive command loop.

    Args:
        parser (CommandParser): Command parser instance
        rover (Rover): Rover instance
        in_stream (TextIO): Input stream (typically stdin)
        out_stream (TextIO): Output stream (typically stdout)
    """
    out_stream.write("Mars Rover Simulator\n")
    out_stream.write("Commands: PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | EXIT\n\n")
    out_stream.flush()

    while True:
        try:
            out_stream.write("> ")
            out_stream.flush()
            line = in_stream.readline()
            if not line:
                out_stream.write("\nGoodbye!\n")
                return

            user_input = line.strip()
            if not user_input:
                continue

            if user_input.upper() == "EXIT":
                out_stream.write("Goodbye!\n")
                return

            command = parser.parse(user_input)
            result = command.execute(rover)

            if isinstance(result, CommandResult):
                if not result.success:
                    out_stream.write(f"Error: {result.message}\n")
            elif isinstance(result, str):
                out_stream.write(f"{result}\n")

        except RoverException as e:
            out_stream.write(f"Error: {e}\n")
        except KeyboardInterrupt:
            out_stream.write("\nGoodbye!\n")
            return


def main() -> None:
    """Main entry point for the application."""
    bounds = TableBounds()
    rover = Rover(bounds=bounds)
    parser = CommandParser()
    run_cli_loop(parser, rover, sys.stdin, sys.stdout)
