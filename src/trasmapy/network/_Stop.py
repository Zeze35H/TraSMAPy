from abc import abstractmethod

from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy.users.StopType import StopType


class Stop(IdentifiedObject):
    stopType: StopType = StopType.DEFAULT

    def __init__(self, stopId: str) -> None:
        super().__init__(stopId)

    @property
    @abstractmethod
    def lane(self):
        pass

    @property
    @abstractmethod
    def startPos(self) -> float:
        pass

    @property
    @abstractmethod
    def endPos(self) -> float:
        pass
