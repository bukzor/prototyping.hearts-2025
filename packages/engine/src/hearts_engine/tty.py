"""TTY formatting protocol and utilities."""

import sys
from typing import Protocol
from typing import runtime_checkable


@runtime_checkable
class SupportsTTY(Protocol):
    """Protocol for objects that support colored terminal output."""

    def __tty__(self) -> str: ...


def format(obj: object, *, tty: bool | None = None) -> str:
    """Format object for output, using __tty__ when appropriate."""
    if tty is None:
        tty = sys.stdout.isatty()
    if tty and isinstance(obj, SupportsTTY):
        return obj.__tty__()
    return str(obj)
