import sys
from typing import TextIO

from mars_rover.models import TableBounds
from mars_rover.rover import Rover
from mars_rover.parser import CommandParser


def run_cli_loop(
    parser: CommandParser, rover: Rover, in_stream: TextIO, out_stream: TextIO
) -> None:
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
            if result:
                out_stream.write(f"{result}\n")

        except (ValueError, RuntimeError) as e:
            out_stream.write(f"Error: {e}\n")
        except KeyboardInterrupt:
            out_stream.write("\nGoodbye!\n")
            return


def main() -> None:
    bounds = TableBounds()
    rover = Rover(bounds=bounds)
    parser = CommandParser()
    run_cli_loop(parser, rover, sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
