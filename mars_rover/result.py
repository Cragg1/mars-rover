"""Result objects for command execution."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CommandResult:
    """Result of a command execution."""

    success: bool
    message: Optional[str] = None

    @classmethod
    def ok(cls, message: Optional[str] = None) -> "CommandResult":
        """Create a successful result."""
        return cls(success=True, message=message)

    @classmethod
    def error(cls, message: str) -> "CommandResult":
        """Create an error result."""
        return cls(success=False, message=message)
