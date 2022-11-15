from trasmapy._IdentifiedObject import IdentifiedObject

class Stop(IdentifiedObject):
    def __init__(self, stopId: str, parentId: str, traciModule) -> None:
        super().__init__(stopId)
        self._parentId = parentId
        self._traciModule = traciModule

    def _setParent(self, parentLane) -> None:
        self._parent = parentLane

    @property
    def parentLane(self):
        return self._parent

    @property
    def name(self) -> str:
        return self._traciModule.getName(self.id) # type: ignore

    @property
    def startPos(self) -> float:
        return self._traciModule.getStartPos(self.id) # type: ignore

    @property
    def endPos(self) -> float:
        return self._traciModule.getEndPos(self.id) # type: ignore

    @property
    def vehicleIds(self) -> list[str]:
        return self._traciModule.getVehicleIDs(self.id) # type: ignore
