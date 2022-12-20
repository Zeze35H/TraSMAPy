#!/usr/bin/env python

from traci._trafficlight import Logic
from trasmapy.control._TLPhase import TLPhase


class TLProgram:
    def __init__(
        self,
        id: str,
        progType: int,
        currentPhaseIndex: int,
        phases: list[TLPhase] = [],
        parameters={},
    ) -> None:
        self._programId = id
        self._progType = progType
        self._currentPhaseIndex = currentPhaseIndex
        self._phases = phases
        self._parameters = parameters

    @classmethod
    def tlProg(cls, prog: Logic):
        phases = [TLPhase.tlPhase(p) for p in prog.phases]
        return cls(
            prog.programID,
            prog.type,
            prog.currentPhaseIndex,
            phases,
            prog.subParameter,
        )

    @property
    def programId(self) -> str:
        """Returns the id of the program."""
        return self._programId

    @property
    def typeP(self) -> int:
        """Returns the type of the program."""
        return self._progType

    @property
    def currentPhaseIndex(self) -> int:
        """Returns the index of the current phase."""
        return self._currentPhaseIndex

    @property
    def phases(self) -> list[TLPhase]:
        """Returns the list of phases."""
        return self._phases.copy()

    @property
    def parameters(self):
        """Returns the a dictionary of parameters."""
        return self._parameters.copy()

    def __repr__(self):
        return (
            "TLProgram(programID='%s', type=%s, currentPhaseIndex=%s, phases=%s, subParameter=%s)"
            % (
                self._programId,
                self._progType,
                self._currentPhaseIndex,
                self._phases,
                self._parameters,
            )
        )
