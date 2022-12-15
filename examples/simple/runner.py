#!/usr/bin/env python


from trasmapy import TraSMAPy, Color, VehicleClass, StopType, ScheduledStop

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    queryStr = "network/edges[self.id == '1to2']/stops"
    traSMAPy.registerQuery("stopsQuery", queryStr, 4)
    traSMAPy.registerQuery(
        "stopsQuery2",
        lambda x: [edge.stops for edge in x["network"].edges if edge.id == "1to2"],
    )

    lane = traSMAPy.network.getLane("1to2_1")
    lane.setDisallowed([VehicleClass.PASSENGER])
    busStop = traSMAPy.network.getStop("bs_0")
    parkingArea = traSMAPy.network.getStop("pa_0")
    laneStop = traSMAPy.network.createLaneStop(lane.id, endPos=100)

    t_2 = traSMAPy.control.getTrafficLight("2")
    print(t_2.state)

    print("---testing---")
    print(t_2.completeRedYellowGreenDef)
    print(t_2.getBlockingVehiclesIds(0))
    print(t_2.getRivalVehiclesIds(0))
    print(t_2.getPriorityVehiclesIds(0))

    e10 = traSMAPy.network.getDetector("e1_0")
    e10.listen(lambda x: print(x))

    busType = traSMAPy.users.getVehicleType("Bus")
    carType = traSMAPy.users.getVehicleType("Car")
    route0 = traSMAPy.users.getRoute("route0")

    #  traSMAPy.publicServices.createFleet("fleet0", route0, busType, [ScheduledStop(laneStop, duration=5)], 10)
    traSMAPy.publicServices.createFleet(
        "fleet0", None, busType, [ScheduledStop(busStop, until=20)], 40
    )

    bus = traSMAPy.users.createVehicle("v0", route0, vehicleType=busType)
    bus.color = Color(112, 3, 0)
    bus.stopFor(laneStop, 20.4)
    for i in range(0, 5):
        traSMAPy.users.createVehicle(f"vehicle{i}", route0, vehicleType=carType)

    while traSMAPy.minExpectedNumber > 0:
        if traSMAPy.step > 20:
            lane.allowAll()
        traSMAPy.doSimulationStep()

        print(traSMAPy.collectedStatistics)
        #print(traSMAPy.query("users/vehicles/vehicleType/length"))
        #print(
        #    traSMAPy.query(
        #        lambda x: [
        #            v.vehicleType.length for v in x["users"].vehicles
        #        ],
        #    )
        #)
    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("hello.sumocfg")
    run(traSMAPy)
