#!/usr/bin/env python


from trasmapy import TraSMAPy, VehicleClass, StopType
from trasmapy.publicservices._FleetStop import FleetStop

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    queryStr =  "network/edges[self.id == '1to2']/stops"
    traSMAPy.registerQuery("stopsQuery",queryStr)

    lane = traSMAPy.network.getLane("1to2_1")
    lane.setDisallowed([VehicleClass.PASSENGER])
    busStop = traSMAPy.network.getStop("bs_0")
    laneStop = traSMAPy.network.createLaneStop("1to2_1", endPos=100)

    e10 = traSMAPy.network.getDetector("e1_0")
    e10.listen(lambda x: print(x))

    busType = traSMAPy.users.getVehicleType("Bus")
    carType = traSMAPy.users.getVehicleType("Car")
    route0 = traSMAPy.users.getRoute("route0")

    #  traSMAPy.publicServices.createFleet("fleet0", route0, busType, [FleetStop(laneStop, 5)], 100, 10, 0)
    traSMAPy.publicServices.createFleet("fleet0", None, busType, [FleetStop(laneStop, 5)], 100, 10, 0)

    #  bus = traSMAPy.users.createVehicle("vehicle0", route0, vehicleType=busType)
    #  bus.stopFor(busStop.id, 20.4, endPos=1, stopTypes=[StopType.BUS_STOP])
    for i in range(0, 5):
        traSMAPy.users.createVehicle(f"vehicle{i}", route0, vehicleType=carType)

    while traSMAPy.minExpectedNumber > 0:
        if traSMAPy.step > 20:
            lane.allowAll()
        traSMAPy.doSimulationStep()

    print(traSMAPy.collectedStatistics)
    print(traSMAPy.query(queryStr))
    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("hello.sumocfg")
    run(traSMAPy)
