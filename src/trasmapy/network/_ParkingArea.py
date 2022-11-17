from typing_extensions import override

from traci import parkingarea

from trasmapy.network._StopLocation import StopLocation
from trasmapy.users.StopType import StopType


class ParkingArea(StopLocation):
    stopType: StopType = StopType.PARKING_AREA

    def __init__(self, parkingAreaId: str) -> None:
        super().__init__(parkingAreaId)

    @property
    @override
    def name(self) -> str:
        return parkingarea.getName(self.id)  # type: ignore

    @property
    @override
    def startPos(self) -> float:
        return parkingarea.getStartPos(self.id)  # type: ignore

    @property
    @override
    def endPos(self) -> float:
        return parkingarea.getEndPos(self.id)  # type: ignore

    @property
    @override
    def vehicleIds(self) -> list[str]:
        return parkingarea.getVehicleIDs(self.id)  # type: ignore
