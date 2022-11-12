from enum import IntEnum


class RemoveReason(IntEnum):
    """Vehicle started teleport"""

    TELEPORT = 0x00
    """Vehicle removed while parking"""
    PARKING = 0x01
    """Vehicle arrived"""
    ARRIVED = 0x02
    """Vehicle was vaporized"""
    VAPORIZED = 0x03
    """Vehicle finished route during teleport"""
    TELEPORT_ARRIVED = 0x04
