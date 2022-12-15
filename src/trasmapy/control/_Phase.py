#!/usr/bin/env python

from traci._trafficlight import Phase
from trasmapy.control import SignalColor

class Phase(Phase):
    def __init__(self, duration, state, minDur=-1, maxDur=-1, next=tuple(), name="") -> None:
        super().__init__(duration, state, minDur, maxDur, next, name)

    @property
    def state(self) -> str:
        return SignalColor(self.state).name

    