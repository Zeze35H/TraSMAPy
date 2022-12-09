from typing_extensions import override

import traci

from trasmapy._SimUpdatable import SimUpdatable
from trasmapy.control._TrafficLight import TrafficLight


class Control(SimUpdatable):
    def __init__(self) -> None:
        pass

    @property
    def trafficlights(self) -> list[TrafficLight]:
        return list(map(lambda id: TrafficLight(id), traci.trafficlight.getIDList()))

    def getTrafficLight(self, id: str) -> TrafficLight:
        return TrafficLight(id)

    @override
    def _doSimulationStep(self, *args, step: int, time: float) -> None:
        pass
