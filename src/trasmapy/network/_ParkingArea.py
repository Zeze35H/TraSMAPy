from traci import parkingarea

from trasmapy.network._Stop import Stop


class ParkingArea(Stop):
    def __init__(self, parkingAreaId: str, parentLane) -> None:
        super().__init__(parkingAreaId, parentLane, parkingarea)
