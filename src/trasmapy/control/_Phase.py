#!/usr/bin/env python

from traci._trafficlight import Phase
from trasmapy.control.SignalColor import SignalColor


class Phase(Phase):
    def __init__(self, duration: int, state: str, minDur: int = -1, maxDur: int = -1, next=tuple(), name: str = "") -> None:
        super().__init__(duration, state, minDur, maxDur, next, name)

    @property
    def duration(self) -> int:
        """Returns the phase's duration (s)."""
        return self.duration

    @property
    def state(self) -> str:
        """Returns the phase's state."""
        return self.state

    @property
    def minDuration(self) -> int:
        """Returns minimum duration (s). Minimum duration applies only to actuated traffic lights. The value is -1 if it does not apply."""
        return self.minDuration

    @property
    def maxDuration(self) -> int:
        """Returns maximum duration (s). Maximum duration applies only to actuated traffic lights. The value is -1 if it does not apply."""
        return self.maxDur

    @property
    def name(self) -> str:
        """Returns the phase's name."""
        return self.name
    
    @duration.setter
    def duration(self, newValue: int):
        """Sets the duration value (s)."""
        self.property = newValue

    @state.setter
    def state(self, colors: list[SignalColor]):
        """Sets the state value."""
        states = "".join(s.value for s in colors)
        self.state = states

    @minDuration.setter
    def minDuration(self, newValue: int):
        """Sets the minimum duration value (s)."""
        self.minDuration = newValue

    @maxDuration.setter
    def maxDuration(self, newValue: int):
        """Sets the maximum duration value (s)."""
        self.maxDuration = newValue

    @name.setter
    def name(self, newValue: str):
        """Sets the name."""
        self.name = newValue