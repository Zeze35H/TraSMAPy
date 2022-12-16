#!/usr/bin/env python

from traci._trafficlight import Logic
from trasmapy.control._Phase import Phase


class TrafficLogic(Logic):
    def __init__(self, id: str, type: int, currentPhaseIndex: int, phases: list[Phase] = None, parameters=None) -> None:
        super().__init__(id, type, currentPhaseIndex, phases, parameters)
