import functools
from typing_extensions import override

import traci

from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy.color._Colorable import Colorable, Color
from trasmapy.network._Stop import Stop
from trasmapy.users.ScheduledStop import ScheduledStop
from trasmapy.users.MoveReason import MoveReason
from trasmapy.users.RemoveReason import RemoveReason
from trasmapy.users.StopType import StopType
from trasmapy.users.VehicleClass import VehicleClass
from trasmapy.users._VehicleType import VehicleType
from trasmapy.users._VehicleStop import VehicleStop


class Vehicle(IdentifiedObject, Colorable):
    @staticmethod
    def _checkVehicleExistance(method):
        @functools.wraps(method)
        def decorated(*args, **kwargs):
            if args[0].isDead():
                raise ValueError(
                    f"The vehicle doesn't exist anymore in the simulation: [vehicleId={args[0].id}]."
                )
            return method(*args, **kwargs)

        return decorated

    def __init__(self, vehicleId: str):
        super().__init__(vehicleId)
        self._dead: bool = False

    @property
    @_checkVehicleExistance
    def vehicleClass(self) -> VehicleClass:
        return VehicleClass(traci.vehicle.getVehicleClass(self.id))

    @property
    @_checkVehicleExistance
    def vehicleType(self) -> VehicleType:
        return VehicleType(traci.vehicle.getTypeID(self.id))  # type: ignore

    @vehicleType.setter
    @_checkVehicleExistance
    def vehicleType(self, newType: VehicleType) -> None:
        """Sets the vehicle type ID."""
        if isinstance(newType, str):
            traci.vehicle.setType(self.id, newType)
        elif isinstance(newType, VehicleType):
            traci.vehicle.setType(self.id, newType.id)
        else:
            raise ValueError("type needs to be a VehicleType instance or a string.")

    @property
    @_checkVehicleExistance
    def emissionClass(self) -> str:
        return traci.vehicle.getEmissionClass(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def shapeClass(self) -> str:
        return traci.vehicle.getShapeClass(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def personCapacity(self) -> int:
        """Returns the person capacity of the vehicle."""
        return traci.vehicle.getPersonCapacity(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def personCount(self) -> int:
        """Returns the number of people inside the vehicle."""
        return traci.vehicle.getPersonNumber(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def speed(self) -> float:
        """Returns the speed of the vehicle within the last step (m/s).
        Error value: -2^30"""
        return traci.vehicle.getSpeed(self.id)  # type: ignore

    @speed.setter
    @_checkVehicleExistance
    def speed(self, newVal: float) -> None:
        """Sets the vehicle speed (m/s). It may drive slower according to the speed mode (safety rules)."""
        if isinstance(newVal, float) or isinstance(newVal, int):
            traci.vehicle.setSpeed(self.id, newVal)
        else:
            raise ValueError("speed needs to be a number (int/float data type).")

    @property
    @_checkVehicleExistance
    def lateralSpeed(self) -> float:
        """Returns the lateral speed of the vehicle within the last step (m/s).
        Error value: -2^30"""
        return traci.vehicle.getLateralSpeed(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def allowedSpeed(self) -> float:
        """Returns the maximum allowed speed of the lane the vehicle is in (m/s)."""
        return traci.vehicle.getAllowedSpeed(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def acceleration(self) -> float:
        """Returns the acceleration in the previous time step (m/s^2)."""
        return traci.vehicle.getAcceleration(self.id)  # type: ignore

    @_checkVehicleExistance
    def setAcceleration(self, newAccel: float, duration: float) -> None:
        """Sets the vehicle acceleration (m/s^2) for the given amount of time."""
        if not (isinstance(newAccel, float) or isinstance(newAccel, int)):
            raise ValueError("Acceleration needs to be a number (int/float data type).")
        if not (isinstance(duration, float) or isinstance(duration, int)):
            raise ValueError("Duration needs to be a number (int/float data type).")
        traci.vehicle.setAcceleration(self.id, newAccel, duration)

    @property
    @_checkVehicleExistance
    def edgeId(self) -> str:
        """Returns the ID of the edge the vehicle was in the previous time step."""
        return traci.vehicle.getRoadID(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def laneId(self) -> str:
        """Returns the ID of the lane the vehicle was in the previous time step."""
        return traci.vehicle.getLaneID(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def drivenDistance(self) -> float:
        """Returns the distance the vehicle has already driven (m).
        Error value: -2^30"""
        return traci.vehicle.getDistance(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def CO2Emissions(self) -> float:
        """Returns the vehicle's CO2 emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getCO2Emission(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def COEmissions(self) -> float:
        """Returns the vehicle's CO emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getCOEmission(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def HCEmissions(self) -> float:
        """Returns the vehicle's HC emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getHCEmission(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def PMxEmissions(self) -> float:
        """Returns the vehicle's PMx emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getPMxEmission(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def NOxEmissions(self) -> float:
        """Returns the vehicle's NOx emissions during this time step (mg/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getNOxEmission(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def fuelConsumption(self) -> float:
        """Returns the vehicle's NOx emissions during this time step (ml/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getFuelConsumption(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def electricityConsumption(self) -> float:
        """Returns the vehicle's electricity consumption during this time step (Wh/s).
        To get the value for one step multiply with the step length.
        Error value: -2^30"""
        return traci.vehicle.getElectricityConsumption(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def noiseEmission(self) -> float:
        """Returns the noise generated by the vehicle (dBA).
        Error value: -2^30"""
        return traci.vehicle.getNoiseEmission(self.id)  # type: ignore

    @property
    @_checkVehicleExistance
    def timeLoss(self) -> float:
        return traci.vehicle.getTimeLoss(self.id)  # type: ignore

    @property
    @override
    @_checkVehicleExistance
    def color(self) -> Color:
        return Color(*traci.vehicle.getColor(self.id))

    @color.setter
    @override
    @_checkVehicleExistance
    def color(self, color: Color) -> None:
        traci.vehicle.setColor(self.id, color.colorTupleA)

    def isDead(self) -> bool:
        return self._dead

    def isPending(self) -> bool:
        return self.id in traci.simulation.getPendingVehicles()

    @_checkVehicleExistance
    def _getStopState(self) -> int:
        return traci.vehicle.getStopState(self.id)  # type: ignore

    def isStoppedAnyReason(self) -> bool:
        """Returns whether the vehicle's is stopped state for any reason (any stopped state)"""
        return self._getStopState() > 0

    def isStopped(self) -> bool:
        """Returns whether the vehicle's stop state is: stopped"""
        return self._getStopState() & (StopType.DEFAULT + 1) != 0

    def isParking(self) -> bool:
        """Returns whether the vehicle's stop state is: parking"""
        return self._getStopState() & (StopType.PARKING << 1) != 0

    def isTriggered(self) -> bool:
        """Returns whether the vehicle's stop state is: triggered"""
        return self._getStopState() & (StopType.TRIGGERED << 1) != 0

    def isContainerTriggered(self) -> bool:
        """Returns whether the vehicle's stop state is: containerTriggered"""
        return self._getStopState() & (StopType.CONTAINER_TRIGGERED << 1) != 0

    def isAtBusStop(self) -> bool:
        """Returns whether the vehicle's stop state is: atBusStop"""
        return self._getStopState() & (StopType.BUS_STOP << 1) != 0

    def isAtContainerStop(self) -> bool:
        """Returns whether the vehicle's stop state is: atContainerStop"""
        return self._getStopState() & (StopType.CONTAINER_STOP << 1) != 0

    def isAtChargingStation(self) -> bool:
        """Returns whether the vehicle's stop state is: atChargingStation"""
        return self._getStopState() & (StopType.CHARGING_STATION << 1) != 0

    def isAtParkingArea(self) -> bool:
        """Returns whether the vehicle's stop state is: atParkingArea"""
        return self._getStopState() & (StopType.PARKING_AREA << 1) != 0

    @_checkVehicleExistance
    def getStops(self) -> list[VehicleStop]:
        stops: list[VehicleStop] = []
        for stopData in traci.vehicle.getStops(self.id):
            stops.append(VehicleStop(stopData))
        return stops

    @_checkVehicleExistance
    def stop(self, scheduledStop: ScheduledStop) -> None:
        """Stops the vehicle at the given location with the given schedule.
        Re-issuing a stop command with the same location allows changing the duration.
        Setting the duration to 0 cancels an existing stop.
        Note that it might not be possible for a vehicle to stop at a given place because of access restrictions."""
        try:
            traci.vehicle.setStop(
                self.id,
                scheduledStop.stop.id,
                laneIndex=scheduledStop.stop.laneIndex,
                pos=scheduledStop.stop.endPos,
                startPos=scheduledStop.stop.startPos,
                duration=scheduledStop.duration,
                until=scheduledStop.until,
                flags=functools.reduce(lambda x, y: x | y, scheduledStop.stopTypes),
            )
        except traci.TraCIException as e:
            raise ValueError(
                f"It isn't possible for the vehicle to stop there: [vehicleId={self.id}], [error={e}]"
            )

    @_checkVehicleExistance
    def stopFor(
        self, stop: Stop, duration: float, stopParams: list[StopType] = []
    ) -> None:
        """Stops the vehicle at the given position in the given edge for the given duration (s).
        See documentation for the stop(...) method."""
        self.stop(ScheduledStop(stop, duration=duration, stopParams=stopParams))

    @_checkVehicleExistance
    def stopUntil(
        self, stop: Stop, until: float, stopParams: list[StopType] = []
    ) -> None:
        """Stops the vehicle at the given position in the given edge until a given simulation time (s).
        See documentation for the stop(...) method."""
        self.stop(ScheduledStop(stop, until=until, stopParams=stopParams))

    def resume(self) -> None:
        """Resumes the march of a stopped vehicle.
        Throws exception if the vehicle isn't stopped."""
        if self.isStoppedAnyReason():
            traci.vehicle.resume(self.id)
        else:
            raise ValueError(
                f"The vehicle isn't stopped, so it can't resume: [vehicleId={self.id}]"
            )

    @_checkVehicleExistance
    def moveTo(
        self, laneId: str, pos: float, reason: MoveReason = MoveReason.AUTOMATIC
    ) -> None:
        """Move a vehicle to a new position along its current route."""
        traci.vehicle.moveTo(self.id, laneId, pos, reason.value)

    @_checkVehicleExistance
    def remove(self, reason: RemoveReason = RemoveReason.VAPORIZED) -> None:
        self._dead = True
        traci.vehicle.remove(self.id, reason=reason)
