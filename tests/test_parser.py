import pytest

from mars_rover.parser import CommandParser
from mars_rover.commands import (
    PlaceCommand,
    MoveCommand,
    LeftCommand,
    RightCommand,
    ReportCommand,
)
from mars_rover.models import Direction
from mars_rover.exceptions import InvalidCommandException


class TestCommandParser:
    def test_parse_move(self):
        parser = CommandParser()
        cmd = parser.parse("MOVE")
        assert isinstance(cmd, MoveCommand)

    def test_parse_left(self):
        parser = CommandParser()
        cmd = parser.parse("LEFT")
        assert isinstance(cmd, LeftCommand)

    def test_parse_right(self):
        parser = CommandParser()
        cmd = parser.parse("RIGHT")
        assert isinstance(cmd, RightCommand)

    def test_parse_report(self):
        parser = CommandParser()
        cmd = parser.parse("REPORT")
        assert isinstance(cmd, ReportCommand)

    def test_parse_case_insensitive(self):
        parser = CommandParser()
        assert isinstance(parser.parse("move"), MoveCommand)
        assert isinstance(parser.parse("MoVe"), MoveCommand)

    def test_parse_with_whitespace(self):
        parser = CommandParser()
        cmd = parser.parse("  MOVE  ")
        assert isinstance(cmd, MoveCommand)

    def test_parse_place_valid(self):
        parser = CommandParser()
        cmd = parser.parse("PLACE 1,2,NORTH")
        assert isinstance(cmd, PlaceCommand)
        assert cmd.args.x == 1
        assert cmd.args.y == 2
        assert cmd.args.direction == Direction.NORTH

    def test_parse_place_all_directions(self):
        parser = CommandParser()
        for direction in ["NORTH", "EAST", "SOUTH", "WEST"]:
            cmd = parser.parse(f"PLACE 0,0,{direction}")
            assert cmd.args.direction == Direction(direction)

    def test_parse_place_with_spaces(self):
        parser = CommandParser()
        cmd = parser.parse("PLACE  1 , 2 , EAST ")
        assert cmd.args.x == 1
        assert cmd.args.y == 2
        assert cmd.args.direction == Direction.EAST

    def test_parse_place_lowercase(self):
        parser = CommandParser()
        cmd = parser.parse("place 3,4,south")
        assert cmd.args.x == 3
        assert cmd.args.y == 4
        assert cmd.args.direction == Direction.SOUTH

    def test_parse_place_missing_args(self):
        parser = CommandParser()
        with pytest.raises(InvalidCommandException, match="exactly 3 arguments"):
            parser.parse("PLACE 1,2")

    def test_parse_place_too_many_args(self):
        parser = CommandParser()
        with pytest.raises(InvalidCommandException, match="exactly 3 arguments"):
            parser.parse("PLACE 1,2,NORTH,EXTRA")

    def test_parse_place_invalid_x(self):
        parser = CommandParser()
        with pytest.raises(InvalidCommandException, match="Invalid PLACE command"):
            parser.parse("PLACE X,2,NORTH")

    def test_parse_place_invalid_y(self):
        parser = CommandParser()
        with pytest.raises(InvalidCommandException, match="Invalid PLACE command"):
            parser.parse("PLACE 1,Y,NORTH")

    def test_parse_place_invalid_direction(self):
        parser = CommandParser()
        with pytest.raises(InvalidCommandException, match="Invalid PLACE command"):
            parser.parse("PLACE 1,2,INVALID")

    def test_parse_unknown_command(self):
        parser = CommandParser()
        with pytest.raises(InvalidCommandException, match="Unknown command"):
            parser.parse("JUMP")

    def test_parse_empty_string(self):
        parser = CommandParser()
        with pytest.raises(InvalidCommandException, match="Unknown command"):
            parser.parse("")
