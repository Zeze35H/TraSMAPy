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
        states = "".join(s.value for s in colors)
        super().__init__(duration, states, minDur, maxDur, next, name)
        self._stateColors = colors

    def setColors(self, colors: list[SignalColor]):
        """Sets the state colors."""
        self._stateColors = colors
        stateStr = "".join(s.value for s in colors)
        self.state = stateStr
