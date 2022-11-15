from traci import busstop

from trasmapy.network._Stop import Stop


class BusStop(Stop):
    def __init__(self, busStopId: str, parentLane) -> None:
        super().__init__(busStopId, parentLane, busstop)

    @property
    def personIds(self) -> list[str]:
        return busstop.getPersonIDs(self.id)  # type: ignore
