#!/usr/bin/env python

from traci._trafficlight import Logic
from trasmapy.control._Phase import Phase

class TrafficLogic(Logic):
    def __init__(self, id: str, type: int, currentPhaseIndex: int, phases=None, subParameter=None) -> None:
        super().__init__(id, type, currentPhaseIndex, phases, subParameter)
    
    @property
    def phases(self) -> list[Phase]:
        return self.phases

    @property
    def type(self) -> int:
        return self.type

    
    