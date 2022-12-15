#!/usr/bin/env python

from traci._trafficlight import Logic
from trasmapy.control._Phase import Phase


class TrafficLogic(Logic):
    def __init__(self, id: str, type: int, currentPhaseIndex: int, phases: list[Phase] = None, parameters=None) -> None:
        super().__init__(id, type, currentPhaseIndex, phases, parameters)

    @property
    def programId(self) -> str:
        """Returns the program Id."""
        return self.getSubID()

    @property
    def type(self) -> int:
        """Returns the type of the program."""
        return self.getType()

    @property
    def currentPhaseIndex(self) -> int:
        """Returns the index of the current phase."""
        return self.currentPhaseIndex

    @property
    def phases(self) -> list[Phase]:
        """Returns the list of phases."""
        return self.getPhases()

    @property
    def parameters(self):
        """Returns the a dictionary of parameters."""
        return self.getParameters()

    @property
    def getParameter(self, key, default=None):
        """Returns the a dictionary of parameters."""
        return self.getParameters(key, default)

    def __repr__(self):
        return ("Logic(programId='%s', type=%s, currentPhaseIndex=%s, phases=%s, parameter=%s)" %
                (self.programId, self.type, self.currentPhaseIndex, self.phases, self.parameters))
