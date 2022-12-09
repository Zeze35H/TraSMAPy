#!/usr/bin/env python


from trasmapy import TraSMAPy


import traci


def run(traSMAPy: TraSMAPy):
    edgeStart = traSMAPy.network.getEdge("64131")
    edgeEnd = traSMAPy.network.getEdge("60697")
    edgeVia = traSMAPy.network.getEdge("-53535")
    edgeEnd2 = traSMAPy.network.getEdge("-33492")

    r = traSMAPy.users.createRouteFromEdges("r0", [edgeStart, edgeEnd])
    v = traSMAPy.users.createVehicle("v0", r)
    v.changeTargetEdge(edgeEnd2)

    v.via = [edgeVia.id]

    """execute the TraCI control loop"""
    while traSMAPy.minExpectedNumber > 0:
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("rand.sumocfg")
    run(traSMAPy)
