#!/usr/bin/env python

from traci._trafficlight import Logic
from trasmapy.control._Phase import Phase


class TrafficLogic(Logic):
    def __init__(
        self,
        id: str,
        type: int,
        currentPhaseIndex: int,
        phases: list[Phase] = None,
        parameters=None,
    ) -> None:
        super().__init__(id, type, currentPhaseIndex, phases, parameters)

    @classmethod
    def traciLogic(cls, prog: Logic):
        return cls(
            prog.programID,
            prog.type,
            prog.currentPhaseIndex,
            prog.phases,
            prog.subParameter,
        )

    def __repr__(self):
        return (
            "TrafficLogic(programID='%s', type=%s, currentPhaseIndex=%s, phases=%s, subParameter=%s)"
            % (
                self.programID,
                self.type,
                self.currentPhaseIndex,
                self.phases,
                self.subParameter,
            )
        )
