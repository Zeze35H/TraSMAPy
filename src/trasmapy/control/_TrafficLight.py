#!/usr/bin/env python

import traci

from trasmapy._IdentifiedObject import IdentifiedObject


class TrafficLight(IdentifiedObject):
    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def state(self) -> str:
        return traci.trafficlight.getRedYellowGreenState(self.id)

    @property
    def phase(self) -> int:
        return traci.trafficlight.getPhase(self.id)

    @property
    def phaseDuration(self) -> float:
        return traci.trafficlight.getPhaseDuration(self.id)

    @property
    def phaseName(self) -> str:
        return traci.trafficlight.getPhaseName(self.id)

    @property
    def nextSwitchTime(self) -> float:
        return traci.trafficlight.getNextSwitch(self.id)

    @property
    def timeTillNextSwitch(self) -> float:
        return traci.trafficlight.getNextSwitch(self.id) - traci.simulation.getTime()

    @property
    def controlledLinkIds(self):
        return traci.trafficlight.getControlledLinks(self.id)

    @property
    def controlledLaneIds(self):
        return traci.trafficlight.getControlledLanes(self.id)

    @property
    def getAllProgramLogics(self):
        return traci.trafficlight.getAllProgramLogics(self.id)
