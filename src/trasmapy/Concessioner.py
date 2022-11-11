from sys import stderr

import traci

# for circular dependency
class _Edge:
    pass

class _Lane:
    def __init__(self, laneId: str, parentEdge: _Edge) -> None:
        self._id = laneId
        self._parent = parentEdge

        self._maxSpeed : float = traci.lane.getMaxSpeed(self._id)

    @property
    def id(self) -> str:
        return self._id

    @property
    def parent(self) -> _Edge:
        return self._parent

    @property
    def maxSpeed(self) -> float:
        return self._maxSpeed

    @maxSpeed.setter
    def maxSpeed(self, newVal):
        """Sets the maximum speed for the vehicles in this lane."""
        if isinstance(newVal, float) or isinstance(newVal, int):
            self._maxSpeed = newVal
            traci.lane.setMaxSpeed(self._id, self._maxSpeed)
        else:
            raise ValueError("maxSpeed needs to be a number (int/float data type).")

    def limitMaxSpeed(self, maxSpeed: float) -> None:
        """Limits the maximum speed for the vehicles in this lane.
        Only changes the value if it needs to be lowered."""
        if maxSpeed < self._maxSpeed:
            self.maxSpeed = maxSpeed

    def setAllowed(self, allowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles allowed to move on this lane."""
        traci.lane.setAllowed(self._id, allowedVehicleClasses)

    def setDisallowed(self, disallowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles disallowed to move on this lane."""
        traci.lane.setDisallowed(self._id, disallowedVehicleClasses)

    def allowAll(self) -> None:
        """Allow all vehicle classes to move on this lane."""
        self.setAllowed(["all"])

    def forbidAll(self) -> None:
        """Forbid all vehicle classes to move on this lane."""
        self.setDisallowed(["all"])


class _Edge:
    def __init__(self, edgeId: str, laneList: list[str]) -> None:
        self._id = edgeId

        self._lanes : dict[str, _Lane] = {}
        for laneId in laneList:
            self._lanes[laneId] = _Lane(laneId, self)
        

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


class Concessioner:
    def __init__(self) -> None:
        # obtain map from l
        edgeToLaneMap : dict[str, list[str]] = {}
        for laneId in traci.lane.getIDList():
            parentEdgeId : str = traci.lane.getEdgeID(laneId)
            try:
                laneList = edgeToLaneMap[parentEdgeId]
                laneList.append(laneId)
            except KeyError:
                edgeToLaneMap[parentEdgeId] = [laneId]

        print(edgeToLaneMap)

        self._edges : dict[str, _Edge] = {} 
        for edgeId in traci.edge.getIDList():
            try:
                laneList = edgeToLaneMap[edgeId]
                self._edges[edgeId] = _Edge(edgeId, laneList)
            except KeyError:
                print(f"Failed to find any lanes for edge (skipping it): [edgeId={edgeId}]",file=stderr)
                continue

    @property
    def edges(self) -> dict[str, _Edge]:
        return self._edges.copy()

    def getEdge(self, edgeId: str) -> _Edge:
        return self._edges[edgeId]

    def getLane(self, laneId: str) -> _Lane:
        for edge in self._edges.values():
            try:
                return edge.getLane(laneId)
            except KeyError:
                continue
        raise KeyError(f"Lane not found: [laneId={laneId}]")
