#!/usr/bin/env python

import traci

from traci._trafficlight import Logic
from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy.control._Link import Link


class TrafficLight(IdentifiedObject):
    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def state(self) -> str:
        """Returns the named traffic lights state."""
        return traci.trafficlight.getRedYellowGreenState(self.id)

    @property
    def phase(self) -> int:
        """Returns the index of the current phase in the currrent program."""
        return traci.trafficlight.getPhase(self.id)

    @property
    def phaseDuration(self) -> float:
        """Returns a default total duration of the active phase (s)."""
        return traci.trafficlight.getPhaseDuration(self.id)

    @property
    def phaseName(self) -> str:
        """Returns the name of the current phase in the current program."""
        return traci.trafficlight.getPhaseName(self.id)

    @property
    def nextSwitchTime(self) -> float:
        """Returns the assumed time at which the TLS changes the phase (s)."""
        return traci.trafficlight.getNextSwitch(self.id)

    @property
    def timeTillNextSwitch(self) -> float:
        """Returns the time left for the next switch (s)."""
        return traci.trafficlight.getNextSwitch(self.id) - traci.simulation.getTime()

    @property
    def controlledLinkIds(self) -> dict[int, list[Link]]:
        """Returns a dictionary of links controlled by the traffic light, where the key is the tls link index of the connection. """

        linkList = traci.trafficlight.getControlledLinks(self.id)
        dictLinks = {}
        for i in range(len(linkList)):
            dictLinks[i] = []
            for links in linkList[i]:
                dictLinks[i] += [Link(links[0], links[1], links[2])]
        
        return dictLinks

    @property
    def controlledLaneIds(self) -> list[str]:
        """Returns the list of lanes which are controlled by the named traffic light. Returns at least one entry for every element of the phase state (signal index)."""
        return traci.trafficlight.getControlledLanes(self.id)

    @property
    def getAllProgramLogics(self) -> list[Logic]:
        """Returns a list of Logic objects."""
        return traci.trafficlight.getAllProgramLogics(self.id)

    @property
    def completeRedYellowGreenDef(self) -> list[Logic]:
        """Returns the complete traffic light program, structure described under data types."""
        return traci.trafficlight.getCompleteRedYellowGreenDefinition(self.id)

    def getBlockingVehiclesIds(self, linkIndex) -> list[str]:
        """Returns the ids of vehicles that occupy the subsequent rail signal block."""
        return traci.trafficlight.getBlockingVehicles(self.id, linkIndex)

    def getRivalVehiclesIds(self, linkIndex) -> list[str]:
        """Returns the ids of vehicles that are approaching the same rail signal block."""
        return traci.trafficlight.getRivalVehicles(self.id, linkIndex)

    def getPriorityVehiclesIds(self, linkIndex) -> list[str]:
        """Returns the ids of vehicles that are approaching the same rail signal block with higher priority."""
        return traci.trafficlight.getPriorityVehicles(self.id, linkIndex)

