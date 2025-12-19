"""Shared type definitions for Hearts engine."""

from typing import Literal

PlayerId = Literal[0, 1, 2, 3]
PLAYER_IDS: tuple[PlayerId, ...] = (0, 1, 2, 3)
