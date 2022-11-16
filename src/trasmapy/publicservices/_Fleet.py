from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy.publicservices._FleetStop import FleetStop


class Fleet(IdentifiedObject):
    def __init__(
        self,
        fleetId: str,
        fleetStops: list[FleetStop],
        end: float,
        period: int,
        start: float = 0,
    ) -> None:
        super().__init__(fleetId)
        self._fleetStops = fleetStops
        self._end = end
        self._period = period
        self._start = start

    @property
    def fleetStops(self) -> list[FleetStop]:
        return self._fleetStops.copy()

    @property
    def end(self) -> float:
        return self._end

    @property
    def period(self) -> float:
        return self._period

    @property
    def start(self) -> float:
        return self._start
