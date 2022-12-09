#!/usr/bin/env python


from trasmapy import TraSMAPy, Color, VehicleClass, StopType, ScheduledStop, MoveReason
import random


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""


    # vehicle types
    defaultVehicle = traSMAPy.users.getVehicleType("DEFAULT_VEHTYPE")
    evehicleType = defaultVehicle.duplicate("evehicle")
    evehicleType.vehicleClass = VehicleClass.EVEHICLE
    evehicleType.color = Color(100, 100, 255)

    # get edges
    e40 = traSMAPy.network.getEdge("E40")
    e9 = traSMAPy.network.getEdge("E9")

    e53 = traSMAPy.network.getEdge("E53")
    e58 = traSMAPy.network.getEdge("E58")
    e48 = traSMAPy.network.getEdge("E48")
    
    e41 = traSMAPy.network.getEdge("E41")
    e41a = traSMAPy.network.getEdge("-E41.28")

    e6 = traSMAPy.network.getEdge("E6")
    e11 = traSMAPy.network.getEdge("-E11")

    e31 = traSMAPy.network.getEdge("E31")

    
    # forbid access to non eletric vehicles
    e41.setDisallowed([defaultVehicle.vehicleClass])
    e41a.setDisallowed([defaultVehicle.vehicleClass])
    # e45.setDisallowed([defaultVehicle.vehicleClass])

    # get prehexisting routes 
    # route0 = traSMAPy.users.getRoute('r_0')  
    # route1 = traSMAPy.users.getRoute('r_1')  

    # setup custom route
    route2 = traSMAPy.users.createRouteFromEdges("r_2", [e40, e9])
    pa_route = traSMAPy.users.createRouteFromEdges("pa_route", [e6, e11])
    pa_1 = traSMAPy.network.getStop('pa_1')

    vs = []
    evs = []
    for i in range(0, 300, 3):
        # schedule parking
        v = traSMAPy.users.createVehicle(f"vehicle{i}", pa_route, defaultVehicle)
        v.stopFor(pa_1, random.randint(1000, 80000), stopParams=[StopType.PARKING])

        vs.append(traSMAPy.users.createVehicle(f"vehicle{i+1}", route2, defaultVehicle))
        evs.append(traSMAPy.users.createVehicle(f"vehicle{i+2}", route2, evehicleType))

    while traSMAPy.minExpectedNumber > 0:
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("sim.sumocfg")
    run(traSMAPy)
