import sys
from mars_rover.models import TableBounds
from mars_rover.rover import Rover
from mars_rover.parser import CommandParser


def main():
    bounds = TableBounds()
    rover = Rover(bounds=bounds)
    parser = CommandParser()

    print("Mars Rover Simulator")
    print("Commands: PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | EXIT")
    print()

    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            if user_input.upper() == "EXIT":
                print("Goodbye!")
                break

            command = parser.parse(user_input)
            result = command.execute(rover)

            if result:
                print(result)

        except (ValueError, RuntimeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
