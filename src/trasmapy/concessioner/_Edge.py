import traci

from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy.concessioner._Lane import Lane
from trasmapy.users.VehicleClass import VehicleClass


class Edge(IdentifiedObject):
    def __init__(self, edgeId: str, laneList: list[str]) -> None:
        super().__init__(edgeId)

        self._lanes: dict[str, Lane] = {}
        for laneId in laneList:
            self._lanes[laneId] = Lane(laneId, self)

    @property
    def streetName(self) -> str:
        """Returns the street name of the edge."""
        return traci.edge.getStreetName(self.id)  # type: ignore

    @property
    def travelTime(self) -> float:
        """Returns the estimated travel time for the last time step on the edge (s)."""
        return traci.edge.getTraveltime(self.id)  # type: ignore

    @property
    def CO2Emissions(self) -> float:
        """Sum of CO2 emissions on this edge during this time step (mg)."""
        return traci.edge.getCO2Emission(self.id)  # type: ignore

    @property
    def COEmissions(self) -> float:
        """Sum of CO emissions on this edge during this time step (mg)."""
        return traci.edge.getCOEmission(self.id)  # type: ignore

    @property
    def HCEmissions(self) -> float:
        """Sum of HC emissions on this edge during this time step (mg)."""
        return traci.edge.getHCEmission(self.id)  # type: ignore

    @property
    def PMxEmissions(self) -> float:
        """Sum of PMx emissions on this edge during this time step (mg)."""
        return traci.edge.getPMxEmission(self.id)  # type: ignore

    @property
    def NOxEmissions(self) -> float:
        """Sum of NOx emissions on this edge during this time step (mg)."""
        return traci.edge.getNOxEmission(self.id)  # type: ignore

    @property
    def fuelConsumption(self) -> float:
        """Sum of fuel consumption on this edge during this time step (ml)."""
        return traci.edge.getFuelConsumption(self.id)  # type: ignore

    @property
    def electricityConsumption(self) -> float:
        """Sum of electricity consumption on this edge during this time step (kWh)."""
        return traci.edge.getElectricityConsumption(self.id)  # type: ignore

    @property
    def vehicleCount(self) -> int:
        """The number of vehicles on this edge within the last time step."""
        return traci.edge.getLastStepVehicleNumber(self.id)  # type: ignore

    @property
    def vehicleMeanSpeed(self) -> float:
        """Returns the mean speed of vehicles that were on this edge within the last simulation step (m/s)."""
        return traci.edge.getLastStepMeanSpeed(self.id)  # type: ignore

    @property
    def vehicleIds(self) -> list[str]:
        """Returns the list of ids of vehicles that were on the edge in the last simulation step.
        The order is from rightmost to leftmost lane and downstream for each lane."""
        return traci.edge.getLastStepVehicleIDs(self.id)  # type: ignore

    @property
    def occupancy(self) -> float:
        """Returns the percentage of time the edge was occupied by a vehicle (%)."""
        return traci.edge.getLastStepOccupancy(self.id)  # type: ignore

    @property
    def vehicleMeanLength(self) -> float:
        """Returns the mean length of the vehicles on the edge in the last time step (m)."""
        return traci.edge.getLastStepLength(self.id)  # type: ignore

    @property
    def vehicleWaitingTime(self) -> float:
        """Returns the sum of the waiting times for all vehicles on the edge (s)."""
        return traci.edge.getWaitingTime(self.id)  # type: ignore

    @property
    def vehicleHaltCount(self) -> int:
        """Returns the total number of halting vehicles for the last time step on the edge.
        A speed of less than 0.1 m/s is considered a halt."""
        return traci.edge.getLastStepHaltingNumber(self.id)  # type: ignore

    @property
    def lanes(self) -> dict[str, Lane]:
        return self._lanes.copy()

    def getLane(self, laneId) -> Lane:
        return self._lanes[laneId]

    def setMaxSpeed(self, maxSpeed: float) -> None:
        """Sets the maximum speed for the vehicles in this edge (for all lanes) to the given value."""
        if isinstance(maxSpeed, float) or isinstance(maxSpeed, int):
            traci.edge.setMaxSpeed(self.id, maxSpeed)
        else:
            raise ValueError("maxSpeed needs to be a number (int/float data type).")

    def limitMaxSpeed(self, maxSpeed: float) -> None:
        """Limits the maximum speed for the vehicles in this edge to the given value.
        Only affects lanes with higher maximum vehicle speeds than the given value."""
        for lane in self._lanes.values():
            lane.limitMaxSpeed(maxSpeed)

    def setAllowed(self, allowedVehicleClasses: list[VehicleClass]) -> None:
        """Set the classes of vehicles allowed to move on this edge."""
        # Note: although traci.edge.setAllowed exists, it isn't recognized by sumo
        for lane in self._lanes.values():
            lane.setAllowed(allowedVehicleClasses)

    def setDisallowed(self, disallowedVehicleClasses: list[VehicleClass]) -> None:
        """Set the classes of vehicles disallowed to move on this edge."""
        for lane in self._lanes.values():
            lane.setDisallowed(disallowedVehicleClasses)

    def allowAll(self) -> None:
        """Allow all vehicle classes to move on this edge."""
        for lane in self._lanes.values():
            lane.allowAll()

    def forbidAll(self) -> None:
        """Forbid all vehicle classes to move on this edge."""
        for lane in self._lanes.values():
            lane.forbidAll()
