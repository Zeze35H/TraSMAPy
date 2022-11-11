#!/usr/bin/env python


from trasmapy import TraSMAPy

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    traci.vehicle.add("vehicle0", "route0", typeID="Car")

    laneId = "1to2_1"
    lane = traSMAPy.concenssioner.getLane(laneId)
    lane.forbidAll()

    while traci.simulation.getMinExpectedNumber() > 0:
        if traSMAPy.step > 20:
            lane.allowAll()
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("hello.sumocfg")
    run(traSMAPy)
