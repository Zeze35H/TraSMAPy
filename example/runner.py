#!/usr/bin/env python


from trasmapy import TraSMAPy

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    laneId = "1to2_1"
    lane = traSMAPy.concenssioner.getLane(laneId)
    #  lane.forbidAll()
    lane.setDisallowed(["passenger"])

    e10 = traSMAPy.concenssioner.getDetector("e1_0")
    e10.listen(lambda x: print(x))

    traci.vehicle.add(
        "vehicle0", "route0", typeID="Car", personNumber=5, personCapacity=10
    )
    print(traci.vehicle.getPersonCapacity("vehicle0"))
    print(traci.vehicle.getPersonNumber("vehicle0"))
    print(traci.vehicle.getVehicleClass("vehicle0"))
    traci.vehicle.setType("vehicle0", "otipo")

    while traSMAPy.minExpectedNumber > 0:
        if traSMAPy.step > 20:
            lane.allowAll()
        traSMAPy.doSimulationStep()
        print(e10.timeSinceLastDetection)

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("hello.sumocfg")
    run(traSMAPy)
