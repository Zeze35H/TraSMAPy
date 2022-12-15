from typing_extensions import override

import traci

from trasmapy._SimUpdatable import SimUpdatable
from trasmapy.control._TrafficLight import TrafficLight
from trasmapy.control.Toll import Toll


class Control(SimUpdatable):
    def __init__(self) -> None:
        self._tolls: dict[str, Toll] = {}

    @property
    def trafficlights(self) -> list[TrafficLight]:
        return list(map(lambda id: TrafficLight(id), traci.trafficlight.getIDList()))

    def getTrafficLight(self, id: str) -> TrafficLight:
        return TrafficLight(id)

    @property
    def tolls(self) -> list[Toll]:
        return list(self._tolls.values())

    def registerToll(self, toll: Toll) -> None:
        if toll.id in self._tolls:
            raise KeyError("There's already a Toll with that ID registered.")
        self._tolls[toll.id] = toll

    def getToll(self, id: str) -> Toll:
        """Returns the registered Toll with the given ID or raises KeyError if none is found."""
        return self._tolls[id]

    @override
    def _doSimulationStep(self, *args, step: int, time: float) -> None:
        pass
