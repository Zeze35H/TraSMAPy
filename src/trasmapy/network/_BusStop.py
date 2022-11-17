from typing_extensions import override

from traci import busstop

from trasmapy.network._StopLocation import StopLocation
from trasmapy.users.StopType import StopType


class BusStop(StopLocation):
    stopType: StopType = StopType.BUS_STOP

    def __init__(self, busStopId: str) -> None:
        super().__init__(busStopId)

    @property
    @override
    def name(self) -> str:
        return busstop.getName(self.id)  # type: ignore

    @property
    @override
    def startPos(self) -> float:
        return busstop.getStartPos(self.id)  # type: ignore

    @property
    @override
    def endPos(self) -> float:
        return busstop.getEndPos(self.id)  # type: ignore

    @property
    @override
    def vehicleIds(self) -> list[str]:
        return busstop.getVehicleIDs(self.id)  # type: ignore

    @property
    def personIds(self) -> list[str]:
        return busstop.getPersonIDs(self.id)  # type: ignore
