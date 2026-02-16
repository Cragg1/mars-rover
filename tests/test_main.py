from io import StringIO
from unittest.mock import Mock
import pytest

from mars_rover.main import run_cli_loop
from mars_rover.models import TableBounds
from mars_rover.rover import Rover
from mars_rover.parser import CommandParser


class TestCLI:
    @pytest.fixture
    def cli_runner(self):
        def _run(script):
            out = StringIO()
            run_cli_loop(CommandParser(), Rover(TableBounds()), StringIO(script), out)
            return out.getvalue()

        return _run

    def test_place_move_report(self, cli_runner):
        output = cli_runner("PLACE 0,0,NORTH\nMOVE\nREPORT\nEXIT\n")
        assert "0,1,NORTH" in output

    def test_place_left_report(self, cli_runner):
        output = cli_runner("PLACE 0,0,NORTH\nLEFT\nREPORT\nEXIT\n")
        assert "0,0,WEST" in output

    def test_multiple_moves_and_turns(self, cli_runner):
        output = cli_runner("PLACE 1,2,EAST\nMOVE\nMOVE\nLEFT\nMOVE\nREPORT\nEXIT\n")
        assert "3,3,NORTH" in output

    def test_invalid_command_then_recover(self, cli_runner):
        output = cli_runner("JUMP\nPLACE 1,2,EAST\nREPORT\nEXIT\n")
        assert "Error:" in output
        assert "1,2,EAST" in output

    def test_eof_exits_gracefully(self, cli_runner):
        output = cli_runner("")
        assert "Goodbye!" in output

    def test_empty_input_ignored(self, cli_runner):
        output = cli_runner("\n\n\nPLACE 0,0,NORTH\nREPORT\nEXIT\n")
        assert "0,0,NORTH" in output

    def test_keyboard_interrupt(self):
        parser = CommandParser()
        rover = Rover(TableBounds())
        in_stream = Mock()
        in_stream.readline.side_effect = KeyboardInterrupt()
        out = StringIO()
        run_cli_loop(parser, rover, in_stream, out)
        assert "Goodbye!" in out.getvalue()

    def test_report_outputs_string(self, cli_runner):
        output = cli_runner("PLACE 2,3,SOUTH\nREPORT\nEXIT\n")
        assert "2,3,SOUTH" in output

    def test_successful_move_no_output(self, cli_runner):
        output = cli_runner("PLACE 0,0,NORTH\nMOVE\nEXIT\n")
        assert "Error:" not in output
        assert "Goodbye!" in output
