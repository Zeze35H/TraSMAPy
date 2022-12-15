#!/usr/bin/env python

import traci

from traci._trafficlight import Logic
from trasmapy.control._TrafficLogic import TrafficLogic
from trasmapy.control._Link import Link
from trasmapy.control.SignalColor import SignalColor
from trasmapy._IdentifiedObject import IdentifiedObject


class TrafficLight(IdentifiedObject):
    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def state(self) -> str:
        """Returns the named traffic lights state."""
        return traci.trafficlight.getRedYellowGreenState(self.id)

    @property
    def phaseId(self) -> int:
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
        """Returns the absolute simulation time at which the traffic light is schedule to switch to the next phase (s)."""
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
    def programLogics(self) -> list[Logic]:
        """Returns the list of programs of the traffic light. Each progam is encoded as a Logic object."""
        return traci.trafficlight.getAllProgramLogics(self.id)

    @property
    def programId(self) -> str:
        """"Returns the id of the current program."""
        return traci.trafficlight.getProgram(self.id)

    @property
    def program(self) -> TrafficLogic:
        """"Returns the current program."""
        return self.getProgram(self.programId)

    def getProgram(self, programId: str) -> TrafficLogic:
        """Returns the program with the given id."""
        for prog in self.programLogics:
            if prog.programID == programId:
                return prog
        return None

    def getBlockingVehiclesIds(self, linkIndex) -> list[str]:
        """Returns the ids of vehicles that occupy the subsequent rail signal block."""
        return traci.trafficlight.getBlockingVehicles(self.id, linkIndex)

    def getRivalVehiclesIds(self, linkIndex) -> list[str]:
        """Returns the ids of vehicles that are approaching the same rail signal block."""
        return traci.trafficlight.getRivalVehicles(self.id, linkIndex)

    def getPriorityVehiclesIds(self, linkIndex) -> list[str]:
        """Returns the ids of vehicles that are approaching the same rail signal block with higher priority."""
        return traci.trafficlight.getPriorityVehicles(self.id, linkIndex)

    @phaseId.setter
    def phaseId(self, phaseIndex: int):
        """Sets the phase of the traffic light to the phase with the given index. The index must be
        valid for the current program of the traffic light."""
        if not self.isPhaseInProgram(self.programId, phaseIndex):
            raise ValueError("The given index is not valid for the current program.")
    
        traci.trafficlight.setPhase(self.id, phaseIndex)

    @phaseDuration.setter
    def phaseDuration(self, newValue: float):
        """Sets the remaining duration of the current phase (s)."""
        if newValue < 0: 
            raise ValueError("Time must be greater than 0.")
        traci.trafficlight.setPhaseDuration(self.id, newValue)

    @programId.setter
    def programId(self, programId: str):
        """Switches to the program with the given programId."""
        if not self.getProgram(programId):
            raise ValueError("A program with the given programID does not exist ofr the traffic light.")
        traci.trafficlight.setProgram(self.id, programId)

    @program.setter
    def program(self, newProg: TrafficLogic) -> TrafficLogic:
        """Switches the traffic light to a new program. The program is directly instantiated."""
        traci.trafficlight.setProgram(self.id, newProg)

    def setRedYellowGreenState(self, colors: list[SignalColor]):
        """Sets the phase definition. Accepts a list of SignalColors that represnt light definitions.
        After this call, the program of the traffic light will be set to online, and the state will be maintained until the next
        call of setRedYellowGreenState() or until setting another program with setProgram()"""
        states = "".join(s.value for s in colors)
        traci.trafficlight.setRedYellowGreenState(self.id, states)

    def turnOff(self):
        """Turns off the traffic light."""
        traci.trafficlight.setProgram(self.id, "off")

    def isPhaseInProgram(self, programId: str, phaseIndex: int) -> bool:
        """Returns true if the program with the given Id contains a phase with at the given index."""
        prog = self.getProgram(programId)
        return 0 <= phaseIndex < len(prog.phases) 
       