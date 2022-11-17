from datetime import timedelta
from time import strptime
from typing import Union

from traci.constants import INVALID_DOUBLE_VALUE

from trasmapy.network._Stop import Stop
from trasmapy.users.StopType import StopType


class ScheduledStop:
    def __init__(
        self,
        stop: Stop,
        duration: Union[float, str] = 0.0,
        until: Union[float, str] = INVALID_DOUBLE_VALUE,
        stopParams: list[StopType] = [],
    ) -> None:
        """Represents a stop schedule. Useful to add a stop for a vehicle.
        BUS_STOP, CONTAINER_STOP, CHARGING_STATION, PARKING_AREA, and DEFAULT can't be combined (stop types).
        Some stop types might ignore the stop positions (follow their own rules).
        PARKING - if present, the vehicle doesn't stop on the road (invisible in the simulation).
        TRIGGERED - if present, the stop has to be manually ended.
        """
        self._stop = stop
        self._stopParams = stopParams
        self._duration = (
            self._timeStr2Sec(duration) if isinstance(duration, str) else duration
        )
        self._until = self._timeStr2Sec(until) if isinstance(until, str) else until
        self._initialUntil = self._until

        self._checkParamsValidaty()

    @property
    def stop(self) -> Stop:
        return self._stop

    @property
    def stopParams(self) -> list[StopType]:
        return self._stopParams.copy()

    @property
    def stopTypes(self) -> list[StopType]:
        return [self._stop.stopType] + self._stopParams

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def until(self) -> float:
        return self._until

    def hasDuration(self) -> bool:
        return self._duration != 0.0

    def hasUntilTime(self) -> bool:
        return self._until != INVALID_DOUBLE_VALUE

    def shiftUntilTime(self, timeReference: float) -> None:
        """Changes the until time of the ScheduledStop to start counting after the given timeReference.
        Useful when establishing public transport schedules: the until time of transports after the first
        should start counting on the moment it has departed."""
        if self.hasUntilTime():
            self._until = self._initialUntil + timeReference

    def _timeStr2Sec(self, timeStr: str) -> float:
        x = strptime(timeStr, "%H:%M:%S")
        return timedelta(
            hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec
        ).total_seconds()

    def _checkParamsValidaty(self):
        if self._stop.stopType == StopType.BUS_STOP:
            if not all(
                x not in self._stopParams
                for x in [
                    StopType.DEFAULT,
                    StopType.CONTAINER_STOP,
                    StopType.CHARGING_STATION,
                ]
            ):
                raise ValueError(
                    f"Bus stops can't be associated with any of the following params: Default, ContainerStop, ChargingStation."
                )
        elif self._stop.stopType == StopType.CHARGING_STATION:
            if not all(
                x not in self._stopParams
                for x in [
                    StopType.DEFAULT,
                    StopType.CONTAINER_STOP,
                    StopType.BUS_STOP,
                ]
            ):
                raise ValueError(
                    f"Charging stations can't be associated with any of the following params: Default, ContainerStop, BusStop."
                )
        elif self._stop.stopType == StopType.DEFAULT:
            if not all(
                x not in self._stopParams
                for x in [
                    StopType.CHARGING_STATION,
                    StopType.CONTAINER_STOP,
                    StopType.BUS_STOP,
                ]
            ):
                raise ValueError(
                    f"Edge/Lane parking can't be associated with any of the following params: ChargingStation, ContainerStop, BusStop."
                )
        elif self._stop.stopType == StopType.PARKING_AREA:
            if not all(
                x not in self._stopParams
                for x in [
                    StopType.DEFAULT,
                    StopType.CONTAINER_STOP,
                    StopType.BUS_STOP,
                ]
            ):
                raise ValueError(
                    f"Parking areas can't be associated with any of the following params: Default, ContainerStop, BusStop."
                )
