from traci import chargingstation

from trasmapy.network._Stop import Stop


class ChargingStation(Stop):
    def __init__(self, chargingStationId: str, parentLane) -> None:
        super().__init__(chargingStationId, parentLane, chargingstation)
