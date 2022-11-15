from sys import stderr
from itertools import chain

import traci

from trasmapy.network._Edge import Edge
from trasmapy.network._Lane import Lane
from trasmapy.network._Stop import Stop
from trasmapy.network._Detector import Detector
from trasmapy.users.StopType import StopType


class Network:
    def __init__(self) -> None:
        # obtain map from l
        edgeToLaneMap: dict[str, list[str]] = {}
        for laneId in traci.lane.getIDList():
            parentEdgeId: str = traci.lane.getEdgeID(laneId)  # type: ignore
            try:
                laneList = edgeToLaneMap[parentEdgeId]
                laneList.append(laneId)
            except KeyError:
                edgeToLaneMap[parentEdgeId] = [laneId]

        laneToStopMap: dict[str, list[tuple[StopType, str]]] = {}
        self._mapStops(laneToStopMap, StopType.BUS_STOP, traci.busstop)
        self._mapStops(laneToStopMap, StopType.CHARGING_STATION, traci.chargingstation)
        self._mapStops(laneToStopMap, StopType.PARKING_AREA, traci.parkingarea)

        self._edges: dict[str, Edge] = {}
        for edgeId in traci.edge.getIDList():
            try:
                laneList = edgeToLaneMap[edgeId]
                self._edges[edgeId] = Edge(edgeId, laneList, laneToStopMap)
            except KeyError:
                print(
                    f"Failed to find any lanes for edge (skipping it): [edgeId={edgeId}]",
                    file=stderr,
                )
                continue

        self._detectors: dict[str, Detector] = {}

    def _mapStops(self, map, prefix: StopType, traciModule):
        for stopId in traciModule.getIDList():
            parentLaneId: str = traciModule.getLaneID(stopId)  # type: ignore
            try:
                stopList = map[stopId]
                stopList.append((prefix, stopId))
            except KeyError:
                map[parentLaneId] = [stopId]

    @property
    def edges(self) -> dict[str, Edge]:
        """Returns a list of all edges in the network."""
        return self._edges.copy()

    @property
    def stops(self) -> dict[str, list[Stop]]:
        """A map from edgeId to its stops (in its lanes)."""
        ret: dict[str, list[Stop]] = {}
        for edge in self._edges.values():
            edgeStops = edge.stops.values()
            if len(edgeStops) > 0:
                ret[edge.id] = list(chain(*edgeStops))
        return ret

    def getEdge(self, edgeId: str) -> Edge:
        """Returns an object representing the edge with the given ID in the network.
        Raises KeyError if the given edge doesn't exist."""
        return self._edges[edgeId]

    def getLane(self, laneId: str) -> Lane:
        """Returns an object representing the lane with the given ID in the network.
        Raises KeyError if the given lane doesn't exist in any edge."""
        # TODO if this func causes performance problems: create index from laneId to Edge
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
