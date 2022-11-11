#!/usr/bin/env python


from trasmapy import TraSMAPy

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    traci.vehicle.add("vehicle0", "route0", typeID="Car")

    laneId = "1to2_1"
    lane = traSMAPy.concenssioner.getLane(laneId)
    lane.forbidAll()

    e10 = traSMAPy.concenssioner.getDetector("e1_0")
    e10.listen(lambda x: print(x))

    while traci.simulation.getMinExpectedNumber() > 0:
        if traSMAPy.step > 20:
            lane.allowAll()
        traSMAPy.doSimulationStep()
        print(e10.timeSinceLastDetection)

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("hello.sumocfg")
    run(traSMAPy)
