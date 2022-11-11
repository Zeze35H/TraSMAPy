from sys import stderr

import traci

from trasmapy.concessioner._Edge import Edge
from trasmapy.concessioner._Lane import Lane
from trasmapy.concessioner._Detector import Detector


class Concessioner:
    def __init__(self) -> None:
        # obtain map from l
        edgeToLaneMap : dict[str, list[str]] = {}
        for laneId in traci.lane.getIDList():
            parentEdgeId : str = traci.lane.getEdgeID(laneId)
            try:
                laneList = edgeToLaneMap[parentEdgeId]
                laneList.append(laneId)
            except KeyError:
                edgeToLaneMap[parentEdgeId] = [laneId]

        self._edges : dict[str, Edge] = {} 
        for edgeId in traci.edge.getIDList():
            try:
                laneList = edgeToLaneMap[edgeId]
                self._edges[edgeId] = Edge(edgeId, laneList)
            except KeyError:
                print(f"Failed to find any lanes for edge (skipping it): [edgeId={edgeId}]",file=stderr)
                continue

        self._detectors : dict[str, Detector] = {}

    @property
    def edges(self) -> dict[str, Edge]:
        """Returns a list of all edges in the network."""
        return self._edges.copy()

    def getEdge(self, edgeId: str) -> Edge:
        """Returns an object representing the edge with the given ID in the network.
        Raises KeyError if the given edge doesn't exist."""
        return self._edges[edgeId]

    def getLane(self, laneId: str) -> Lane:
        """Returns an object representing the lane with the given ID in the network.
        Raises KeyError if the given lane doesn't exist in any edge."""
        for edge in self._edges.values():
            try:
                return edge.getLane(laneId)
            except KeyError:
                continue
        raise KeyError(f"Lane not found: [laneId={laneId}]")

    def getDetector(self, detectorId: str) -> Detector:
        """Returns an object representing the inductionloop (E1) with the given ID in the network.
        Raises KeyError if the given inductionloop doesn't exist in any lane."""
        try:
            return self._detectors[detectorId]
        except KeyError:
            if detectorId in traci.inductionloop.getIDList():
                det = Detector(detectorId)
                self._detectors[detectorId] = det
                return det
        raise KeyError(f"Detector not found: [detectorId={detectorId}]")

    def _doSimulationStep(self) -> None:
        for detector in self._detectors.values():
            detector._doSimulationStep()
