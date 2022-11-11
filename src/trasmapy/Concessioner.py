from sys import stderr

import traci

from trasmapy._Edge import Edge
from trasmapy._Lane import Lane


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

    @property
    def edges(self) -> dict[str, Edge]:
        return self._edges.copy()

    def getEdge(self, edgeId: str) -> Edge:
        return self._edges[edgeId]

    def getLane(self, laneId: str) -> Lane:
        for edge in self._edges.values():
            try:
                return edge.getLane(laneId)
            except KeyError:
                continue
        raise KeyError(f"Lane not found: [laneId={laneId}]")
