import traci

class Edge:
    pass

class Lane:
    def __init__(self, laneId: str, parentEdge: Edge) -> None:
        self._id = laneId
        self._parent = parentEdge

        self._maxSpeed : float = traci.lane.getMaxSpeed(self._id)

    @property
    def id(self) -> str:
        return self._id

    @property
    def parent(self) -> Edge:
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
