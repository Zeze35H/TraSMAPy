from traci._vehicle import StopData
from traci.constants import INVALID_DOUBLE_VALUE

from trasmapy.users.StopType import StopType


class VehicleStop():
    def __init__(self, stopData: StopData) -> None:
        self._stopId: str = stopData.stoppingPlaceID
        self._duration: float = stopData.duration
        self._until: float = stopData.until
        self._arrival: float = stopData.arrival
        self._intendedArrival: float = stopData.intendedArrival
        self._depart: float = stopData.depart

        self._stopTypes: list[StopType] = []
        for stopType in StopType:
            if stopData.stopFlags & stopType != 0:
                self._stopTypes.append(stopType)


    @property
    def stop(self) -> str:
        return self._stopId

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def until(self) -> float:
        return self._until

    @property
    def arrival(self) -> float:
        return self._arrival

    def hasArrived(self) -> bool:
        return self.arrival != INVALID_DOUBLE_VALUE

    @property
    def intendedArrival(self) -> float:
        return self._intendedArrival

    @property
    def depart(self) -> float:
        return self._depart

    def hasDeparted(self) -> bool:
        return self.depart != INVALID_DOUBLE_VALUE

    @property
    def stopTypes(self) -> list[StopType]:
        return self._stopTypes

    def __repr__(self):
        return f"VehicleStop(stopId={self.stop}, duration={self.duration}, until={self.until}, types={self.stopTypes})"

