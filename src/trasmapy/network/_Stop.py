from trasmapy._IdentifiedObject import IdentifiedObject

class Stop(IdentifiedObject):
    def __init__(self, stopId: str, parentLane, traciModule) -> None:
        super().__init__(stopId)
        self._parent = parentLane
        self._traciModule = traciModule

    @property
    def name(self) -> str:
        return self._traciModule.getName(self.id) # type: ignore

    @property
    def lane(self):
        return self._parent

    @property
    def startPos(self) -> float:
        return self._traciModule.getStartPos(self.id) # type: ignore

    @property
    def endPos(self) -> float:
        return self._traciModule.getEndPos(self.id) # type: ignore

    @property
    def vehicleIds(self) -> list[str]:
        return self._traciModule.getVehicleIDs(self.id) # type: ignore
