from enum import IntEnum


class MoveReason(IntEnum):
    """Infer reason from move distance."""

    AUTOMATIC = 0x00

    """Vehicle teleports to another location"""
    TELEPORT = 0x01

    """vehicle moved normally"""
    NORMAL = 0x02
