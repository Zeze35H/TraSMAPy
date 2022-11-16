from sys import stderr
from typing_extensions import override

import traci


from trasmapy._SimUpdatable import SimUpdatable
from trasmapy.network._Edge import Edge
from trasmapy.network._Lane import Lane
from trasmapy.network._Stop import Stop
from trasmapy.network._Detector import Detector
from trasmapy.network._BusStop import BusStop
from trasmapy.network._ChargingStation import ChargingStation
from trasmapy.network._ParkingArea import ParkingArea


class Network(SimUpdatable):
    def __init__(self) -> None:
        # index Stops
        self._stopsIndex: dict[str, Stop] = {}
        laneToStopMap: dict[str, list[Stop]] = {}
        self._indexStops(laneToStopMap, BusStop, traci.busstop)
        self._indexStops(laneToStopMap, ChargingStation, traci.chargingstation)
        self._indexStops(laneToStopMap, ParkingArea, traci.parkingarea)

        # index Lanes
        self._lanesIndex: dict[str, Lane] = {}
        edgeToLaneMap: dict[str, list[Lane]] = {}
        for laneId in traci.lane.getIDList():
            try:
                stopList = laneToStopMap[laneId]
            except KeyError:
                stopList = []

            parentEdgeId: str = traci.lane.getEdgeID(laneId)  # type: ignore
            lane = Lane(laneId, stopList)
            self._lanesIndex[laneId] = lane
            try:
                edgeToLaneMap[parentEdgeId].append(lane)
            except KeyError:
                edgeToLaneMap[parentEdgeId] = [lane]

        # index edges
        self._edges: dict[str, Edge] = {}
        for edgeId in traci.edge.getIDList():
            try:
                laneList = edgeToLaneMap[edgeId]
                self._edges[edgeId] = Edge(edgeId, laneList)
            except KeyError:
                print(
                    f"Failed to find any lanes for edge (skipping it): [edgeId={edgeId}]",
                    file=stderr,
                )
                continue

        self._detectors: dict[str, Detector] = {}

    def _indexStops(self, laneToStopMap, StopClass, traciModule):
        for stopId in traciModule.getIDList():
            parentLaneId: str = traciModule.getLaneID(stopId)  # type: ignore
            stop: Stop = StopClass(stopId, parentLaneId)
            self._stopsIndex[stopId] = stop
            try:
                laneToStopMap[parentLaneId].append(stop)
            except KeyError:
                laneToStopMap[parentLaneId] = [stop]

    @property
    def edges(self) -> list[Edge]:
        """Returns a list of all edges in the network."""
        return list(self._edges.values())

    @property
    def lanes(self) -> list[Lane]:
        """Returns a list of all edges in the network."""
        return list(self._lanesIndex.values())

    @property
    def stops(self) -> list[Stop]:
        """Returns a list of all stops in the network."""
        return list(self._stopsIndex.values())

    def getEdge(self, edgeId: str) -> Edge:
        """Returns an object representing the edge with the given ID in the network.
        Raises KeyError if the given edge doesn't exist."""
        return self._edges[edgeId]

    def getLane(self, laneId: str) -> Lane:
        """Returns an object representing the lane with the given ID in the network.
        Raises KeyError if the given lane doesn't exist in any edge."""
        return self._lanesIndex[laneId]

    def getStop(self, stopId: str) -> Stop:
        """Returns an object representing the lane with the given ID in the network.
        Raises KeyError if the given lane doesn't exist in any edge."""
        return self._stopsIndex[stopId]

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

    @override
    def _doSimulationStep(self, *args, step: int, time: float) -> None:
        for detector in self._detectors.values():
            detector._doSimulationStep(args, step=step, time=time)
