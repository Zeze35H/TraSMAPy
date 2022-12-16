#!/usr/bin/env python

from traci._trafficlight import Logic
from trasmapy.control._Phase import Phase


class TrafficLogic(Logic):
    def __init__(self, id: str, type: int, currentPhaseIndex: int, phases: list[Phase] = None, parameters=None) -> None:
        super().__init__(id, type, currentPhaseIndex, phases, parameters)

    def __repr__(self):
        return ("Logic(programId='%s', type=%s, currentPhaseIndex=%s, phases=%s, parameter=%s)" %
                (self.programId, self.type, self.currentPhaseIndex, self.phases, self.parameters))
