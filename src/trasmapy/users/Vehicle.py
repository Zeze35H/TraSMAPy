import traci

from trasmapy._IdentifiedObject import IdentifiedObject


class Vehicle(IdentifiedObject):
    def __init__(self, vehicleId: str):
        super().__init__(vehicleId)

    @property
    def vehicleClass(self) -> str:
        return traci.vehicle.getVehicleClass(self.id) # type: ignore

    @vehicleClass.setter
    def vehicleClass(self, newVehicleClass: str) -> None:
        """Sets the vehicle abstact class."""
        if isinstance(newVehicleClass, str):
            traci.vehicle.setVehicleClass(self.id, newVehicleClass)
        else:
            raise ValueError("type needs to be a string.")

    @property
    def type(self) -> str:
        return traci.vehicle.getTypeID(self.id) # type: ignore

    @type.setter
    def type(self, newTypeId: str) -> None:
        """Sets the vehicle type ID."""
        if isinstance(newTypeId, str):
            traci.vehicle.setType(self.id, newTypeId)
        else:
            raise ValueError("type needs to be a string.")

    @property
    def emissionClass(self) -> str:
        return traci.vehicle.getEmissionClass(self.id) # type: ignore

    @property
    def shapeClass(self) -> str:
        return traci.vehicle.getShapeClass(self.id) # type: ignore

    @property
    def personCapacity(self) -> int:
        """Returns the person capacity of the vehicle."""
        return traci.vehicle.getPersonCapacity(self.id) # type: ignore

    @property
    def personCount(self) -> int:
        """Returns the number of people inside the vehicle."""
        return traci.vehicle.getPersonNumber(self.id) # type: ignore

    @property
    def speed(self) -> float:
        """Returns the speed of the vehicle within the last step (m/s).
        Error value: -2^30"""
        return traci.vehicle.getSpeed(self.id) # type: ignore

    @speed.setter
    def speed(self, newVal: float) -> None:
        """Sets the vehicle speed (m/s). It may drive slower according to the speed mode (safety rules)."""
        if isinstance(newVal, float) or isinstance(newVal, int):
            traci.vehicle.setSpeed(self.id, newVal)
        else:
            raise ValueError("speed needs to be a number (int/float data type).")

    @property
    def lateralSpeed(self) -> float:
        """Returns the lateral speed of the vehicle within the last step (m/s).
        Error value: -2^30"""
        return traci.vehicle.getLateralSpeed(self.id) # type: ignore

    @property
    def acceleration(self) -> float:
        """Returns the acceleration in the previous time step (m/s^2)."""
        return traci.vehicle.getAcceleration(self.id) # type: ignore

    @acceleration.setter
    def acceleration(self, newAccel: float, duration: float) -> None:
        """Sets the vehicle acceleration (m/s^2) for the given amount of time."""
        if not (isinstance(newAccel, float) or isinstance(newAccel, int)):
            raise ValueError("Acceleration needs to be a number (int/float data type).")
        if not (isinstance(duration, float) or isinstance(duration, int)):
            raise ValueError("Duration needs to be a number (int/float data type).")
        traci.vehicle.setAcceleration(self.id, newAccel, duration)

    @property
    def edgeId(self) -> str:
        """Returns the ID of the edge the vehicle was in the previous time step."""
        return traci.vehicle.getRoadID(self.id) # type: ignore

    @property
    def laneId(self) -> str:
        """Returns the ID of the lane the vehicle was in the previous time step."""
        return traci.vehicle.getLaneID(self.id) # type: ignore

    @property
    def drivenDistance(self) -> float:
        """Returns the distance the vehicle has already driven (m).
        Error value: -2^30"""
        return traci.vehicle.getDistance(self.id) # type: ignore

    @property
    def CO2Emissions(self) -> float:
        """Returns the vehicle's CO2 emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getCO2Emission(self.id) # type: ignore

    @property
    def COEmissions(self) -> float:
        """Returns the vehicle's CO emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getCOEmission(self.id) # type: ignore

    @property
    def HCEmissions(self) -> float:
        """Returns the vehicle's HC emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getHCEmission(self.id) # type: ignore

    @property
    def PMxEmissions(self) -> float:
        """Returns the vehicle's PMx emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getPMxEmission(self.id) # type: ignore

    @property
    def NOxEmissions(self) -> float:
        """Returns the vehicle's NOx emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getNOxEmission(self.id) # type: ignore

    @property
    def fuelConsumption(self) -> float:
        """Returns the vehicle's NOx emissions during this time step (ml/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getFuelConsumption(self.id) # type: ignore

    @property
    def electricityConsumption(self) -> float:
        """Returns the vehicle's electricity consumption during this time step (Wh/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getElectricityConsumption(self.id) # type: ignore

    @property
    def noiseEmission(self) -> float:
        """Returns the noise generated by the vehicle (dBA).
        Error value: -2^30"""
        return traci.vehicle.getNoiseEmission(self.id) # type: ignore

    @property
    def timeLoss(self) -> float:
        return traci.vehicle.getTimeLoss(self.id) # type: ignore

    def _getStopState(self) -> int:
        return traci.vehicle.getStopState(self.id) # type: ignore

    def isStopped(self) -> bool:
        """Returns whether the vehicle's stop state is: stopped"""
        return self._getStopState() & 1 != 0

    def isParking(self) -> bool:
        """Returns whether the vehicle's stop state is: parking"""
        return self._getStopState() & 2 != 0

    def isTriggered(self) -> bool:
        """Returns whether the vehicle's stop state is: triggered"""
        return self._getStopState() & 4 != 0

    def isContainerTriggered(self) -> bool:
        """Returns whether the vehicle's stop state is: containerTriggered"""
        return self._getStopState() & 8 != 0

    def isAtBusStop(self) -> bool:
        """Returns whether the vehicle's stop state is: atBusStop"""
        return self._getStopState() & 16 != 0

    def isAtContainerStop(self) -> bool:
        """Returns whether the vehicle's stop state is: atContainerStop"""
        return self._getStopState() & 32 != 0

    def isAtChargingStation(self) -> bool:
        """Returns whether the vehicle's stop state is: atChargingStation"""
        return self._getStopState() & 64 != 0

    def isAtParkingArea(self) -> bool:
        """Returns whether the vehicle's stop state is: atParkingArea"""
        return self._getStopState() & 128 != 0

    def stopFor(self, duration: float, edgeId: str, pos: float = 1) -> None:
        """Stops the vehicle at the given position in the given edge for the given duration (s)."""
        traci.vehicle.setStop(self.id, edgeId, pos, duration=duration)

    def stopUntil(self, until: float, edgeId: str, pos: float = 1) -> None:
        """Stops the vehicle at the given position in the given edge until a given simulation time (s)."""
        traci.vehicle.setStop(self.id, edgeId, pos, until=until)
