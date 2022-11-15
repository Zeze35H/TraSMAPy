from enum import IntEnum


class StopType(IntEnum):
    DEFAULT = 0x00
    """Stops on the lane."""

    PARKING = 0x01
    """Whether the vehicle stops on the road or beside."""

    TRIGGERED = 0x02
    """Whether a person may end the stop."""

    CONTAINER_TRIGGERED = 0x04

    BUS_STOP = 0x08
    """If given, containerStop, chargingStation, edge, lane, startPos and endPos are not allowed."""

    CONTAINER_STOP = 0x10
    """If given, busStop, chargingStation, edge, lane, startPos and endPos are not allowed."""

    CHARGING_STATION = 0x20
    """If given, busStop, containerStop, edge, lane, startPos and endPos are not allowed."""

    # TODO
    PARKING_AREA = 0x40
    """Stops at a parking area. See: https://sumo.dlr.de/docs/Simulation/ParkingArea.html#letting_vehicles_stop_at_a_parking_area."""

    OVERHEAD_WIRE = 0x80
