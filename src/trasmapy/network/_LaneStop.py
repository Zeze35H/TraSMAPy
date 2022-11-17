from typing_extensions import override

from traci.constants import INVALID_DOUBLE_VALUE

from trasmapy.network._Stop import Stop
from trasmapy.network._Lane import Lane
from trasmapy.network._Edge import Edge
from trasmapy.users.StopType import StopType


class LaneStop(Stop):
    stopType: StopType = StopType.DEFAULT

    def __init__(
        self, lane: Lane, endPos: float = 0, startPos: float = INVALID_DOUBLE_VALUE
    ) -> None:
        parentEdge: Edge = lane.parentEdge
        super().__init__(parentEdge.id)
        self._lane = lane
        self._laneIndex: int = parentEdge.lanes.index(lane)
        self._endPos: float = endPos
        self._startPos: float = startPos

    @property
    @override
    def laneIndex(self) -> int:
        """The lane index to stop at.
        Traci uses the pair (edge ID, lane index) for lane stops (instead of lane ID). There isn't a way to
        get the index of a lane in traci. As such, we use the index of the order at which lanes are found.
        If a user wants to, it is possible to define lanes' indexes, in the simulation's XML files, in an
        order that doesn't match their positions in the lane. If this happens, the lane index used for the
        stop can match with a different lane (in the same edge)."""
        return self._laneIndex

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
