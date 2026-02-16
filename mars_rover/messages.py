"""Error messages."""


class ErrorMessages:
    """Error messages for rover commands."""

    ROVER_NOT_PLACED = "Rover must be placed on the table first"
    POSITION_OUT_OF_BOUNDS = (
        "Invalid PLACE command: position ({x},{y}) is outside table bounds"
    )
    MOVE_OUT_OF_BOUNDS = "Invalid MOVE command: would move rover outside table bounds"
    UNKNOWN_COMMAND = "Unknown command: '{command}'"
    PLACE_REQUIRES_ARGS = "PLACE requires exactly 3 arguments: PLACE X,Y,F"
    INVALID_PLACE_COMMAND = "Invalid PLACE command: {text}"
