import traci

from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy.users.VehicleClass import VehicleClass


class Lane(IdentifiedObject):
    def __init__(self, laneId: str, parentEdge) -> None:
        super().__init__(laneId)
        self._parent = parentEdge

    @property
    def parent(self):
        return self._parent

    @property
    def linkCount(self) -> int:
        """Returns the number of links outgoing from this lane."""
        return traci.lane.getLinkNumber(self.id)  # type: ignore

    @property
    def length(self) -> float:
        """Returns the length of the named lane (m)."""
        return traci.lane.getLength(self.id)  # type: ignore

    @length.setter
    def length(self, newLen: float) -> None:
        """Sets the the lane's length."""
        if isinstance(newLen, float) or isinstance(newLen, int):
            traci.lane.setLength(self.id, newLen)
        else:
            raise ValueError("Length needs to be a number (int/float data type).")

    @property
    def width(self) -> float:
        """Returns the width of the named lane (m)."""
        return traci.lane.getWidth(self.id)  # type: ignore

    @property
    def CO2Emissions(self) -> float:
        """Sum of CO2 emissions on this lane in mg during this time step (mg)."""
        return traci.lane.getCO2Emission(self.id)  # type: ignore

    @property
    def COEmissions(self) -> float:
        """Sum of CO emissions on this lane in mg during this time step (mg)."""
        return traci.lane.getCOEmission(self.id)  # type: ignore

    @property
    def HCEmissions(self) -> float:
        """Sum of HC emissions on this lane in mg during this time step (mg)."""
        return traci.lane.getHCEmission(self.id)  # type: ignore

    @property
    def PMxEmissions(self) -> float:
        """Sum of PMx emissions on this lane in mg during this time step (mg)."""
        return traci.lane.getPMxEmission(self.id)  # type: ignore

    @property
    def NOxEmissions(self) -> float:
        """Sum of NOx emissions on this lane in mg during this time step (mg)."""
        return traci.lane.getNOxEmission(self.id)  # type: ignore

    @property
    def fuelConsumption(self) -> float:
        """Sum of fuel consumption on this lane in ml during this time step (ml)."""
        return traci.lane.getFuelConsumption(self.id)  # type: ignore

    @property
    def noiseEmissions(self) -> float:
        """Sum of noise generated on this lane (dBA)."""
        return traci.lane.getNoiseEmission(self.id)  # type: ignore

    @property
    def electricityConsumption(self) -> float:
        """Sum of electricity consumption on this edge during this time step (kWh)."""
        return traci.lane.getElectricityConsumption(self.id)  # type: ignore

    @property
    def vehicleCount(self) -> int:
        """The number of vehicles on this lane within the last time step."""
        return traci.lane.getLastStepVehicleNumber(self.id)  # type: ignore

    @property
    def vehicleMeanSpeed(self) -> float:
        """Returns the mean speed of vehicles that were on this lane within the last simulation step (m/s)"""
        return traci.lane.getLastStepMeanSpeed(self.id)  # type: ignore

    @property
    def vehicleIds(self) -> list[str]:
        """Returns the list of ids of vehicles that were on this lane in the last simulation step."""
        return traci.lane.getLastStepVehicleIDs(self.id)  # type: ignore

    @property
    def occupancy(self) -> float:
        """Returns the total lengths of vehicles on this lane during the last simulation step divided by the length of this lane (%)."""
        return traci.lane.getLastStepOccupancy(self.id)  # type: ignore

    @property
    def vehicleMeanLength(self) -> float:
        """Returns the mean length of the vehicles which were on this lane in the last step (m)."""
        return traci.lane.getLastStepLength(self.id)  # type: ignore

    @property
    def vehicleWaitingTime(self) -> float:
        """Returns the sum of the waiting times for all vehicles on the lane (s)."""
        return traci.lane.getWaitingTime(self.id)  # type: ignore

    @property
    def travelTime(self) -> float:
        """Returns the estimated travel time for the last time step on the given lane (s)."""
        return traci.lane.getTraveltime(self.id)  # type: ignore

    @property
    def vehicleHaltCount(self) -> int:
        """Returns the total number of halting vehicles for the last time step on the given lane.
        A speed of less than 0.1 m/s is considered a halt."""
        return traci.lane.getLastStepHaltingNumber(self.id)  # type: ignore

    @property
    def maxSpeed(self) -> float:
        """Returns the maximum speed allowed on this lane (m/s)."""
        return traci.lane.getMaxSpeed(self.id)  # type: ignore

    @maxSpeed.setter
    def maxSpeed(self, newVal):
        """Sets the maximum speed for the vehicles in this lane."""
        if isinstance(newVal, float) or isinstance(newVal, int):
            traci.lane.setMaxSpeed(self.id, newVal)
        else:
            raise ValueError("maxSpeed needs to be a number (int/float data type).")

    def limitMaxSpeed(self, maxSpeed: float) -> None:
        """Limits the maximum speed for the vehicles in this lane.
        Only changes the value if it needs to be lowered."""
        if maxSpeed < self.maxSpeed:
            self.maxSpeed = maxSpeed

    def allowedVehicles(self) -> list[VehicleClass]:
        """List of allowed vehicle classes on this lane."""
        return list(map(lambda x: VehicleClass(x), traci.lane.getAllowed(self.id)))

    def disallowedVehicles(self) -> list[VehicleClass]:
        """List of disallowed vehicle classes on this lane."""
        return list(map(lambda x: VehicleClass(x), traci.lane.getDisallowed(self.id)))

    def _setAllowed(self, allowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles allowed to move on this lane."""
        traci.lane.setAllowed(self.id, allowedVehicleClasses)

    def _setDisallowed(self, disallowedVehicleClasses: list[str]) -> None:
        """Set the classes of vehicles disallowed to move on this lane."""
        traci.lane.setDisallowed(self.id, disallowedVehicleClasses)

    def setAllowed(self, allowedVehicleClasses: list[VehicleClass]) -> None:
        """Set the classes of vehicles allowed to move on this lane."""
        self._setAllowed(list(map(lambda x: x.value, allowedVehicleClasses)))

    def setDisallowed(self, disallowedVehicleClasses: list[VehicleClass]) -> None:
        """Set the classes of vehicles disallowed to move on this lane."""
        self._setDisallowed(list(map(lambda x: x.value, disallowedVehicleClasses)))

    def allowAll(self) -> None:
        """Allow all vehicle classes to move on this lane."""
        self._setAllowed(["all"])

    def forbidAll(self) -> None:
        """Forbid all vehicle classes to move on this lane."""
        self._setDisallowed(["all"])
