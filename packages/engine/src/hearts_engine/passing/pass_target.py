"""Pass target calculation."""

from ..types import api as T


def pass_target(player: T.PlayerId, direction: T.PassDirection) -> T.PlayerId:
    """Get the target player for passing."""
    match direction:
        case T.PassDirection.LEFT:
            offset = 1
        case T.PassDirection.RIGHT:
            offset = 3
        case T.PassDirection.ACROSS:
            offset = 2
        case T.PassDirection.HOLD:
            return player  # No passing
    return T.player_id(player + offset)
