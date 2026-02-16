import pytest

from mars_rover.models import Direction, Position, TableBounds, PlaceArgs


class TestDirection:
    def test_left_from_north(self):
        assert Direction.NORTH.left() == Direction.WEST

    def test_left_from_west(self):
        assert Direction.WEST.left() == Direction.SOUTH

    def test_left_from_south(self):
        assert Direction.SOUTH.left() == Direction.EAST

    def test_left_from_east(self):
        assert Direction.EAST.left() == Direction.NORTH

    def test_right_from_north(self):
        assert Direction.NORTH.right() == Direction.EAST

    def test_right_from_east(self):
        assert Direction.EAST.right() == Direction.SOUTH

    def test_right_from_south(self):
        assert Direction.SOUTH.right() == Direction.WEST

    def test_right_from_west(self):
        assert Direction.WEST.right() == Direction.NORTH


class TestPosition:
    def test_create_position(self):
        pos = Position(1, 2)
        assert pos.x == 1
        assert pos.y == 2

    def test_position_immutable(self):
        pos = Position(1, 2)
        with pytest.raises(AttributeError):
            pos.x = 3


class TestTableBounds:
    def test_default_bounds(self):
        bounds = TableBounds()
        assert bounds.min_x == 0
        assert bounds.min_y == 0
        assert bounds.max_x == 5
        assert bounds.max_y == 5

    def test_contains_within_bounds(self):
        bounds = TableBounds()
        assert bounds.contains(Position(0, 0))
        assert bounds.contains(Position(5, 5))
        assert bounds.contains(Position(2, 3))

    def test_contains_outside_bounds(self):
        bounds = TableBounds()
        assert not bounds.contains(Position(-1, 0))
        assert not bounds.contains(Position(0, -1))
        assert not bounds.contains(Position(6, 0))
        assert not bounds.contains(Position(0, 6))

    def test_custom_bounds(self):
        bounds = TableBounds(min_x=1, min_y=1, max_x=10, max_y=10)
        assert bounds.contains(Position(1, 1))
        assert bounds.contains(Position(10, 10))
        assert not bounds.contains(Position(0, 0))


class TestPlaceArgs:
    def test_valid_place_args(self):
        args = PlaceArgs(x=1, y=2, direction=Direction.NORTH)
        assert args.x == 1
        assert args.y == 2
        assert args.direction == Direction.NORTH
