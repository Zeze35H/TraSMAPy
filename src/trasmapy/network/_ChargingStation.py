from typing_extensions import override

from traci import chargingstation

from trasmapy.network._StopLocation import StopLocation
from trasmapy.users.StopType import StopType


class ChargingStation(StopLocation):
    stopType: StopType = StopType.CHARGING_STATION

    def __init__(self, chargingStationId: str) -> None:
        super().__init__(chargingStationId)

    @property
    @override
    def name(self) -> str:
        return chargingstation.getName(self.id)  # type: ignore

    @property
    @override
    def startPos(self) -> float:
        return chargingstation.getStartPos(self.id)  # type: ignore

    @property
    @override
    def endPos(self) -> float:
        return chargingstation.getEndPos(self.id)  # type: ignore

    @property
    @override
    def vehicleIds(self) -> list[str]:
        return chargingstation.getVehicleIDs(self.id)  # type: ignore
