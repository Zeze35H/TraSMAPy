from typing_extensions import override

from traci.constants import INVALID_DOUBLE_VALUE

from trasmapy.network._Stop import Stop
from trasmapy.network._Lane import Lane
from trasmapy.users.StopType import StopType


class LaneStop(Stop):
    stopType: StopType = StopType.DEFAULT

    def __init__(
        self, lane: Lane, endPos: float = 0, startPos: float = INVALID_DOUBLE_VALUE
    ) -> None:
        super().__init__(lane.parentEdge.id)
        self._lane = lane
        self._endPos: float = endPos
        self._startPos: float = startPos

    @property
    @override
    def lane(self) -> Lane:
        return self._lane

    @property
    @override
    def startPos(self) -> float:
        return self._startPos

    @property
    @override
    def endPos(self) -> float:
        return self._endPos
