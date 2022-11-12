#!/usr/bin/env python


from trasmapy import TraSMAPy, VehicleClass

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    laneId = "1to2_1"
    lane = traSMAPy.concenssioner.getLane(laneId)
    #  lane.forbidAll()
    lane.setDisallowed([VehicleClass.PASSENGER])

    e10 = traSMAPy.concenssioner.getDetector("e1_0")
    e10.listen(lambda x: print(x))

    v0 = traSMAPy.users.createVehicle(
        "vehicle0", "route0", typeId="Car", personNumber=5, personCapacity=10
    )
    v1 = traSMAPy.users.createVehicle(
        "vehicle1", "route0", typeId="Car", personNumber=5, personCapacity=10
    )
    v2 = traSMAPy.users.createVehicle(
        "vehicle2", "route0", typeId="Car", personNumber=5, personCapacity=10
    )
    v3 = traSMAPy.users.createVehicle(
        "vehicle3", "route0", typeId="Car", personNumber=5, personCapacity=10
    )

    print(traci.vehicletype.getIDList())

    while traSMAPy.minExpectedNumber > 0:
        if traSMAPy.step > 20:
            lane.allowAll()

        print(traci.vehicle.getAllowedSpeed("vehicle0"))
        print(traci.vehicle.getSpeed("vehicle0"))
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("hello.sumocfg")
    run(traSMAPy)
