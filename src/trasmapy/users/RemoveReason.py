from enum import IntEnum


class RemoveReason(IntEnum):
    TELEPORT = 0x00
    """Vehicle started teleport"""
    PARKING = 0x01
    """Vehicle removed while parking"""
    ARRIVED = 0x02
    """Vehicle arrived"""
    VAPORIZED = 0x03
    """Vehicle was vaporized"""
    TELEPORT_ARRIVED = 0x04
    """Vehicle finished route during teleport"""
