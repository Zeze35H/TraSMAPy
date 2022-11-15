from enum import IntEnum


class MoveReason(IntEnum):
    AUTOMATIC = 0x00
    """Infer reason from move distance."""

    TELEPORT = 0x01
    """Vehicle teleports to another location"""

    NORMAL = 0x02
    """vehicle moved normally"""
