from io import StringIO
import pytest

from mars_rover.main import run_cli_loop
from mars_rover.models import TableBounds
from mars_rover.rover import Rover
from mars_rover.parser import CommandParser


@pytest.fixture
def cli_runner():
    def _run(script):
        out = StringIO()
        run_cli_loop(CommandParser(), Rover(TableBounds()), StringIO(script), out)
        return out.getvalue()

    return _run


def test_place_move_report(cli_runner):
    output = cli_runner("PLACE 0,0,NORTH\nMOVE\nREPORT\nEXIT\n")
    assert "0,1,NORTH" in output


def test_place_left_report(cli_runner):
    output = cli_runner("PLACE 0,0,NORTH\nLEFT\nREPORT\nEXIT\n")
    assert "0,0,WEST" in output


def test_multiple_moves_and_turns(cli_runner):
    output = cli_runner("PLACE 1,2,EAST\nMOVE\nMOVE\nLEFT\nMOVE\nREPORT\nEXIT\n")
    assert "3,3,NORTH" in output


def test_invalid_command_then_recover(cli_runner):
    output = cli_runner("JUMP\nPLACE 1,2,EAST\nREPORT\nEXIT\n")
    assert "Error:" in output
    assert "1,2,EAST" in output


def test_eof_exits_gracefully(cli_runner):
    output = cli_runner("")
    assert "Goodbye!" in output
