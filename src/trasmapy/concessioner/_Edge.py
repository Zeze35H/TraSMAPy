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
    def lanes(self):
        return self._lanes.copy()

    def getLane(self, laneId):
        return self._lanes[laneId]

    @property
    def laneNumber(self):
        return self._lanes.len;
    
    @property
    def streetName(self): 
        return traci.edge.getStreetName(self.id)

    @property
    def traveltime(self):
        return traci.edge.getTraveltime(self.id)

    @property
    def CO2Emission(self):
        return traci.edge.getCO2Emission(self.id)

    @property
    def COEmission(self):
        return traci.edge.getCOEmission(self.id)
    
    @property
    def HCEmission(self):
        return traci.edge.getHCEmission(self.id)

    @property
    def PMxEmission(self):
        return traci.edge.getPMxEmission(self.id)

    @property
    def NOxEmissions(self):
        return traci.edge.getNOxEmission(self.id)

    @property
    def fuelConsumption(self):
        return traci.edge.getFuelConsumption(self.id)

    @property
    def noiseEmission(self):
        return traci.edge.getFuelConsumption(self.id)

    @property
    def electricityConsumption(self):
        return traci.edge.getElectricityConsumption(self.id)

    @property
    def lastStepVehicleNumber(self):
        return traci.edge.getLastStepVehicleNumber(self.id)

    @property
    def lastStepMeanSpeed(self):
        return traci.edge.getLastStepMeanSpeed(self.id) 

    @property
    def lastStepVehicleIDs(self):
        return traci.edge.getLastStepVehicleIDs(self.id)

    @property
    def lastStepOccupancy(self):
        return traci.edge.getLastStepOccupancy(self.id)

    @property
    def lastStepLength(self):
        return traci.edge.getLastStepLength(self.id)

    @property
    def waitingTime(self):
        return traci.edge.getWaitingTime(self.id)

    @property
    def lastStepPersonIDs(self):
        return traci.edge.getLastStepPersonIDs(self.id)

    @property
    def lastStepHaltingNumber(self):
        return traci.edge.getLastStepHaltingNumber(self.id)

    def setMaxSpeed(self, maxSpeed: float) -> None:
        """Sets the maximum speed for the vehicles in this edge (for all lanes) to the given value."""
        # Can't use traci directly because Lane state needs to be updated: traci.edge.setMaxSpeed(self.id, maxSpeed)
        for lane in self._lanes.values():
            lane.maxSpeed = maxSpeed

    def limitMaxSpeed(self, maxSpeed: float) -> None:
        """Limits the maximum speed for the vehicles in this edge to the given value.
        Only affects lanes with higher maximum vehicle speeds than the given value."""
        for lane in self._lanes.values():
            lane.limitMaxSpeed(maxSpeed)

    def _setAllowed(self, allowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles allowed to move on this edge."""
        traci.lane.setAllowed(self.id, allowedVehicleClasses)

    def _setDisallowed(self, disallowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles disallowed to move on this edge."""
        traci.lane.setDisallowed(self.id, disallowedVehicleClasses)

    def setAllowed(self, allowedVehicleClasses: list[VehicleClass]) -> None:
        """Set the classes of vehicles allowed to move on this edge."""
        self._setAllowed(list(map(lambda x: x.value, allowedVehicleClasses)))

    def setDisallowed(self, disallowedVehicleClasses: list[VehicleClass]) -> None:
        """Set the classes of vehicles disallowed to move on this edge."""
        self._setDisallowed(list(map(lambda x: x.value, disallowedVehicleClasses)))

    def allowAll(self) -> None:
        """Allow all vehicle classes to move on this edge."""
        self._setAllowed(["all"])

    def forbidAll(self) -> None:
        """Forbid all vehicle classes to move on this edge."""
        self._setDisallowed(["all"])
