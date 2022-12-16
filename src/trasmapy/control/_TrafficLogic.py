#!/usr/bin/env python

from traci._trafficlight import Logic
from trasmapy.control._Phase import Phase


class TrafficLogic:
    def __init__(
        self,
        id: str,
        type: int,
        currentPhaseIndex: int,
        phases: list[Phase] = None,
        parameters=None,
    ) -> None:
        self.programId = id
        self.type = type
        self.currentPhaseIndex = currentPhaseIndex
        self.phases = phases
        self.parameters = parameters

    @classmethod
    def traciLogic(cls, prog: Logic):
        return cls(
            prog.programID,
            prog.type,
            prog.currentPhaseIndex,
            prog.phases,
            prog.subParameter,
        )

    @property
    def type(self) -> int:
        """Returns the type of the program."""
        return self.type

    @property
    def currentPhaseIndex(self) -> int:
        """Returns the index of the current phase."""
        return self.currentPhaseIndex

    @property
    def phases(self) -> list[Phase]:
        """Returns the list of phases."""
        return self.phases

    @property
    def parameters(self):
        """Returns the a dictionary of parameters."""
        return self.parameters

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
