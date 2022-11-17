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
        self._stop = stop
        self._stopParams = stopParams
        self._duration = (
            self._timeStr2Sec(duration) if isinstance(duration, str) else duration
        )
        self._until = self._timeStr2Sec(until) if isinstance(until, str) else until
        self._initialUntil = self._until

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
