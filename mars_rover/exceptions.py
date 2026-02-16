"""Domain-specific exceptions for rover operations."""


class RoverException(Exception):
    """Base exception for rover operations."""


class RoverNotPlacedException(RoverException):
    """Raised when rover operation attempted before placement."""


class InvalidCommandException(RoverException):
    """Raised when command is invalid or malformed."""
