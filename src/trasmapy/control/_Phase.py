#!/usr/bin/env python

from traci._trafficlight import Phase
from trasmapy.control.SignalColor import SignalColor


class Phase(Phase):
    def __init__(
        self,
        duration: int,
        colors: list[SignalColor],
        minDur: int = -1,
        maxDur: int = -1,
        next=tuple(),
        name: str = "",
    ) -> None:
        super().__init__(duration, "", minDur, maxDur, next, name)
        self.setState(colors)


    def setState(self, colors: list[SignalColor]):
        states = "".join(s.value for s in colors)
        self.state = states
