"""Type definitions for system-related data structures."""

from typing import Literal, Protocol

OpenTextMode = Literal['r', 'w', 'a']


class Writable(Protocol):
    """Protocol for writable objects that can accept string messages."""

    def write(self, message: str) -> None:
        """Write a message to the writable object."""
