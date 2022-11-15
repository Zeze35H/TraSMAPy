#!/usr/bin/env python


from trasmapy import TraSMAPy, VehicleClass, StopType

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    lane = traSMAPy.network.getLane("1to2_1")
    lane.setDisallowed([VehicleClass.PASSENGER])

    e10 = traSMAPy.network.getDetector("e1_0")
    e10.listen(lambda x: print(x))

    bus = traSMAPy.users.createVehicle("vehicle0", "route0", typeId="Bus")
    bus.stopFor("bs_0", 10, endPos=1, stopTypes=[StopType.BUS_STOP, StopType.PARKING])
    for i in range(1, 5):
        traSMAPy.users.createVehicle(f"vehicle{i}", "route0", typeId="Car")

    #  print(traci.vehicle.getRouteID("vehicle0"))

    while traSMAPy.minExpectedNumber > 0:
        if traSMAPy.step > 20:
            lane.allowAll()
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("hello.sumocfg")
    run(traSMAPy)
