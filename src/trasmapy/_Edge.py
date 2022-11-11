import traci

from trasmapy._Lane import Lane


class Edge:
    def __init__(self, edgeId: str, laneList: list[str]) -> None:
        self._id = edgeId

        self._lanes : dict[str, Lane] = {}
        for laneId in laneList:
            self._lanes[laneId] = Lane(laneId, self)
        

    @property
    def id(self) -> str:
        return self._id

    @property
    def lanes(self):
        return self._lanes.copy()

    def getLane(self, laneId):
        return self._lanes[laneId]

    def setMaxSpeed(self, maxSpeed: float) -> None:
        """Sets the maximum speed for the vehicles in this edge (for all lanes) to the given value."""
        # Can't use traci directly because Lane state needs to be updated: traci.edge.setMaxSpeed(self._id, maxSpeed)
        for lane in self._lanes.values():
            lane.maxSpeed = maxSpeed

    def limitMaxSpeed(self, maxSpeed: float) -> None:
        """Limits the maximum speed for the vehicles in this edge to the given value.
        Only affects lanes with higher maximum vehicle speeds than the given value."""
        for lane in self._lanes.values():
            lane.limitMaxSpeed(maxSpeed)

    def setAllowed(self, allowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles allowed to move on this edge."""
        traci.lane.setAllowed(self._id, allowedVehicleClasses)

    def setDisallowed(self, disallowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles disallowed to move on this edge."""
        traci.lane.setDisallowed(self._id, disallowedVehicleClasses)

    def allowAll(self) -> None:
        """Allow all vehicle classes to move on this edge."""
        self.setAllowed(["all"])

    def forbidAll(self) -> None:
        """Forbid all vehicle classes to move on this edge."""
        self.setDisallowed(["all"])

