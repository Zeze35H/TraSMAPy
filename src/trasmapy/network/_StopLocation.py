from abc import abstractmethod
from typing_extensions import override

from trasmapy.network._Stop import Stop
from trasmapy.users.StopType import StopType


class StopLocation(Stop):
    stopType: StopType = StopType.DEFAULT

    def __init__(self, stopId: str) -> None:
        super().__init__(stopId)

    def _setParent(self, parentLane) -> None:
        self._parent = parentLane

    @property
    def parentLane(self):
        return self.lane

    @property
    @override
    def lane(self):
        return self._parent

    @property
    def stopTypes(self) -> StopType:
        return self.stopType

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def vehicleIds(self) -> list[str]:
        pass
