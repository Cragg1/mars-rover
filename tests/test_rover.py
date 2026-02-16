import pytest

from mars_rover.rover import Rover
from mars_rover.models import Direction, Position, TableBounds
from mars_rover.exceptions import RoverNotPlacedException


class TestRoverPlace:
    def test_place_valid_position(self):
        rover = Rover(TableBounds())
        result = rover.place(1, 2, Direction.NORTH)
        assert result.success
        assert rover.position == Position(1, 2)
        assert rover.direction == Direction.NORTH

    def test_place_at_origin(self):
        rover = Rover(TableBounds())
        result = rover.place(0, 0, Direction.SOUTH)
        assert result.success
        assert rover.position == Position(0, 0)

    def test_place_at_max_bounds(self):
        rover = Rover(TableBounds())
        result = rover.place(5, 5, Direction.WEST)
        assert result.success
        assert rover.position == Position(5, 5)

    def test_place_outside_bounds(self):
        rover = Rover(TableBounds())
        result = rover.place(6, 0, Direction.NORTH)
        assert not result.success
        assert "outside table bounds" in result.message
        assert rover.position is None

    def test_place_negative_coordinates(self):
        rover = Rover(TableBounds())
        result = rover.place(-1, 0, Direction.NORTH)
        assert not result.success
        assert "outside table bounds" in result.message

    def test_place_replaces_position(self):
        rover = Rover(TableBounds())
        rover.place(1, 1, Direction.NORTH)
        rover.place(2, 2, Direction.SOUTH)
        assert rover.position == Position(2, 2)
        assert rover.direction == Direction.SOUTH


class TestRoverMove:
    def test_move_north(self):
        rover = Rover(TableBounds())
        rover.place(2, 2, Direction.NORTH)
        result = rover.move()
        assert result.success
        assert rover.position == Position(2, 3)

    def test_move_east(self):
        rover = Rover(TableBounds())
        rover.place(2, 2, Direction.EAST)
        result = rover.move()
        assert result.success
        assert rover.position == Position(3, 2)

    def test_move_south(self):
        rover = Rover(TableBounds())
        rover.place(2, 2, Direction.SOUTH)
        result = rover.move()
        assert result.success
        assert rover.position == Position(2, 1)

    def test_move_west(self):
        rover = Rover(TableBounds())
        rover.place(2, 2, Direction.WEST)
        result = rover.move()
        assert result.success
        assert rover.position == Position(1, 2)

    def test_move_without_place(self):
        rover = Rover(TableBounds())
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            rover.move()

    def test_move_blocked_north(self):
        rover = Rover(TableBounds())
        rover.place(0, 5, Direction.NORTH)
        result = rover.move()
        assert not result.success
        assert "outside table bounds" in result.message
        assert rover.position == Position(0, 5)

    def test_move_blocked_south(self):
        rover = Rover(TableBounds())
        rover.place(0, 0, Direction.SOUTH)
        result = rover.move()
        assert not result.success
        assert "outside table bounds" in result.message
        assert rover.position == Position(0, 0)

    def test_move_blocked_east(self):
        rover = Rover(TableBounds())
        rover.place(5, 0, Direction.EAST)
        result = rover.move()
        assert not result.success
        assert "outside table bounds" in result.message
        assert rover.position == Position(5, 0)

    def test_move_blocked_west(self):
        rover = Rover(TableBounds())
        rover.place(0, 0, Direction.WEST)
        result = rover.move()
        assert not result.success
        assert "outside table bounds" in result.message
        assert rover.position == Position(0, 0)


class TestRoverLeft:
    def test_left_without_place(self):
        rover = Rover(TableBounds())
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            rover.left()


class TestRoverRight:
    def test_right_without_place(self):
        rover = Rover(TableBounds())
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            rover.right()


class TestRoverReport:
    def test_report(self):
        rover = Rover(TableBounds())
        rover.place(3, 4, Direction.SOUTH)
        result = rover.report()
        assert result == "3,4,SOUTH"

    def test_report_at_origin(self):
        rover = Rover(TableBounds())
        rover.place(0, 0, Direction.NORTH)
        result = rover.report()
        assert result == "0,0,NORTH"

    def test_report_without_place(self):
        rover = Rover(TableBounds())
        with pytest.raises(RoverNotPlacedException, match="must be placed"):
            rover.report()


class TestRoverCustomBounds:
    def test_custom_bounds(self):
        rover = Rover(TableBounds(min_x=1, min_y=1, max_x=3, max_y=3))
        result = rover.place(0, 0, Direction.NORTH)
        assert not result.success
        assert "outside table bounds" in result.message
        result = rover.place(1, 1, Direction.NORTH)
        assert result.success
