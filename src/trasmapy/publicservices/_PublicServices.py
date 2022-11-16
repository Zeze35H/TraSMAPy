from typing_extensions import override

from trasmapy._SimUpdatable import SimUpdatable
from trasmapy.publicservices._Fleet import Fleet


class PublicServices(SimUpdatable):
    def __init__(self) -> None:
        self._fleets: list[Fleet] = []

    @property
    def fleets(self) -> list[Fleet]:
        return self._fleets

    @override
    def _doSimulationStep(self, step: int, time: float) -> None:
        for fleet in self._fleets:
            fleet._doSimulationStep(step, time)
