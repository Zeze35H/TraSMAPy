from datetime import timedelta
from time import strptime

from traci.constants import INVALID_DOUBLE_VALUE

from trasmapy.network._Stop import Stop


class FleetStop:
    def __init__(
        self,
        stop: Stop,
        duration: float = INVALID_DOUBLE_VALUE,
        until: float = INVALID_DOUBLE_VALUE,
    ) -> None:
        if duration == INVALID_DOUBLE_VALUE and until == INVALID_DOUBLE_VALUE:
            raise ValueError(
                "At least one of duration or until value has to be provided."
            )

        self._stop = stop
        self._duration = (
            self._timeStr2Sec(duration) if isinstance(duration, str) else duration
        )
        self._until = self._timeStr2Sec(until) if isinstance(until, str) else until

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def until(self) -> float:
        return self._until

    def _timeStr2Sec(self, timeStr: str) -> float:
        x = strptime(timeStr, "%H:%M:%S")
        return timedelta(
            hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec
        ).total_seconds()
