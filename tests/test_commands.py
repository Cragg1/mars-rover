import pytest

from mars_rover.commands import (
    PlaceCommand,
    MoveCommand,
    LeftCommand,
    RightCommand,
    ReportCommand,
)
from mars_rover.models import Direction, PlaceArgs, TableBounds
from mars_rover.rover import Rover
from mars_rover.exceptions import RoverNotPlacedException


class TestPlaceCommand:
    def test_place_valid_position(self):
        rover = Rover(TableBounds())
        cmd = PlaceCommand(PlaceArgs(x=1, y=2, direction=Direction.NORTH))
        result = cmd.execute(rover)
        assert result.success
        assert rover.position.x == 1
        assert rover.position.y == 2
        assert rover.direction == Direction.NORTH

    def test_place_outside_bounds(self):
        rover = Rover(TableBounds())
        cmd = PlaceCommand(PlaceArgs(x=10, y=10, direction=Direction.NORTH))
        result = cmd.execute(rover)
        assert not result.success
        assert "outside table bounds" in result.message


class TestMoveCommand:
    def test_move_north(self):
        rover = Rover(TableBounds())
        rover.place(2, 2, Direction.NORTH)
        cmd = MoveCommand()
        result = cmd.execute(rover)
        assert result.success
        assert rover.position.y == 3

    def test_move_without_place(self):
        rover = Rover(TableBounds())
        cmd = MoveCommand()
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            cmd.execute(rover)

    def test_move_outside_bounds(self):
        rover = Rover(TableBounds())
        rover.place(5, 5, Direction.NORTH)
        cmd = MoveCommand()
        result = cmd.execute(rover)
        assert not result.success
        assert "outside table bounds" in result.message
        assert rover.position.y == 5


class TestLeftCommand:
    def test_left_from_north(self):
        rover = Rover(TableBounds())
        rover.place(0, 0, Direction.NORTH)
        cmd = LeftCommand()
        result = cmd.execute(rover)
        assert result.success
        assert rover.direction == Direction.WEST

    def test_left_without_place(self):
        rover = Rover(TableBounds())
        cmd = LeftCommand()
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            cmd.execute(rover)


class TestRightCommand:
    def test_right_from_north(self):
        rover = Rover(TableBounds())
        rover.place(0, 0, Direction.NORTH)
        cmd = RightCommand()
        result = cmd.execute(rover)
        assert result.success
        assert rover.direction == Direction.EAST

    def test_right_without_place(self):
        rover = Rover(TableBounds())
        cmd = RightCommand()
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            cmd.execute(rover)


class TestReportCommand:
    def test_report(self):
        rover = Rover(TableBounds())
        rover.place(3, 4, Direction.SOUTH)
        cmd = ReportCommand()
        result = cmd.execute(rover)
        assert result == "3,4,SOUTH"

    def test_report_without_place(self):
        rover = Rover(TableBounds())
        cmd = ReportCommand()
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            cmd.execute(rover)
