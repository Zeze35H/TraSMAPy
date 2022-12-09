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
    
    e41 = traSMAPy.network.getEdge("E41")
    e41a = traSMAPy.network.getEdge("-E41.28")

    e6 = traSMAPy.network.getEdge("E6")
    e6r = traSMAPy.network.getEdge("-E6")
    
    # forbid access to non eletric vehicles
    e41.setDisallowed([defaultVehicle.vehicleClass])
    e41a.setDisallowed([defaultVehicle.vehicleClass])

    # setup custom route
    route2 = traSMAPy.users.createRouteFromEdges("r_2", [e40, e9])
    pa_route = traSMAPy.users.createRouteFromEdges("pa_route", [e6, e6r])
    
    parking_areas = [traSMAPy.network.getStop(f'pa_{x}') for x in range(0, 5)]
    
    vs = []
    for i in range(0, 300, 3):
        # schedule parking
        v = traSMAPy.users.createVehicle(f"vehicle{i}", pa_route, defaultVehicle)
        park = random.choice(parking_areas)

        v.via = [park.lane.parentEdge.id]

        vehicle_obj = {
            'obj' : v,
            'park' : park
        }
        vs.append(vehicle_obj)

        traSMAPy.users.createVehicle(f"vehicle{i+1}", route2, defaultVehicle)
        traSMAPy.users.createVehicle(f"vehicle{i+2}", route2, evehicleType)

    while traSMAPy.minExpectedNumber > 0:
        traSMAPy.doSimulationStep()
        
        if len(vs) > 0 and traSMAPy.step > 10:
            if vs[0]['obj'].id not in traSMAPy.users.pendingVehicles:
                vs[0]['obj'].stopFor(vs[0]['park'], random.randint(1000, 80000), stopParams=[StopType.PARKING])
                vs.pop(0)

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("sim.sumocfg")
    run(traSMAPy)
