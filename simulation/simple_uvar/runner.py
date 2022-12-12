#!/usr/bin/env python


from trasmapy import TraSMAPy, Color, VehicleClass, StopType, ScheduledStop, MoveReason
import random

def create_route(r_id : str,  edges : list, r_type : str = "normal", 
                 prob : float = None, parks : list = []):
    return {
        "id" : r_id,
        "route" : traSMAPy.users.createRouteFromEdges(r_id, edges),
        "type" : r_type,
        "prob" : prob,
        "park_areas" : parks
    }  
    

def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""

    # vehicle type definition
    defaultVehicle = traSMAPy.users.getVehicleType("DEFAULT_VEHTYPE")
    defaultVehicle.color = Color(200, 200, 200)
    
    evehicleType = defaultVehicle.duplicate("evehicle")
    evehicleType.vehicleClass = VehicleClass.EVEHICLE
    evehicleType.color = Color(50, 50, 255)
    evehicleType.emissionClass = "Energy"
    
    busType = defaultVehicle.duplicate("bus")
    busType.vehicleClass = VehicleClass.BUS
    busType.color = Color(255, 255, 0)
    busType.shape = "bus"


    # get edges
    e40 = traSMAPy.network.getEdge("E40")
    e40r = traSMAPy.network.getEdge("-E40")
    e9 = traSMAPy.network.getEdge("E9")
    
    e41 = traSMAPy.network.getEdge("E41")
    e41a = traSMAPy.network.getEdge("-E41.28")

    e6 = traSMAPy.network.getEdge("E6")
    e6r = traSMAPy.network.getEdge("-E6")
    
    # forbid access to non eletric vehicles
    e41.setDisallowed([defaultVehicle.vehicleClass])
    e41a.setDisallowed([defaultVehicle.vehicleClass])


    PARKING_AREAS_SOUTH = [traSMAPy.network.getStop(f'pa_sw{x}') for x in range(7)]
    PARKING_AREAS_NORTH = [traSMAPy.network.getStop(f"pa_ne{i}") for i in range(14)]

    PARKS = PARKING_AREAS_SOUTH + PARKING_AREAS_NORTH

    V_TYPES = [defaultVehicle, evehicleType]
    
    # setup custom routes
    ROUTES = [
        create_route("r_north_south", [e40, e9], prob=0.1), # NW-SE
        create_route("pa_north", [e40, e40r], r_type="parking", prob=0.6, parks=PARKING_AREAS_NORTH),
        create_route("pa_south", [e6, e6r], r_type="parking", prob=0.3, parks=PARKING_AREAS_NORTH) # SW-SW
    ]
    # TODO fix conflicting park routes
    # TODO semaphores
    
    ROUTE_PROBS = [x["prob"] for x in ROUTES]
    if None in ROUTE_PROBS or sum(ROUTE_PROBS) != 1:
        ROUTE_PROBS = None
        print("Ignoring route probalities.")
        
    # setup public transportation
    bus_stops_r0 = [traSMAPy.network.getStop(f"bs_{i}") for i in range(8)]
    b_route0 = traSMAPy.users.getRoute("bus_se_center")
    traSMAPy.publicServices.createFleet(
        "sw-ne", b_route0, busType, [ScheduledStop(x, 20) for x in bus_stops_r0], period=200, end=4000
    )

    bus_stops_r1 = [traSMAPy.network.getStop(f"bs_ne{i}") for i in range(8)]
    b_route1 = traSMAPy.users.getRoute("bus_ne_center")
    traSMAPy.publicServices.createFleet(
        "ne-center", b_route1, busType, [ScheduledStop(x, 20) for x in bus_stops_r1], period=200, end=4000
    )
    # TODO bus lanes (priority or disallow)

        
    vs_parks = []
    for i in range(0, 800):
        route = random.choices(ROUTES, weights=ROUTE_PROBS, k=1)[0]
        
        v = traSMAPy.users.createVehicle(f"v{i}", route["route"], 
                                            random.choices(V_TYPES, weights=(80, 20), k=1)[0])

        if route["type"] == "parking":
            park = random.choice(route["park_areas"])
            v.via = [park.lane.parentEdge.id]
            vs_parks.append((v, park))

    while traSMAPy.minExpectedNumber > 0:        
        if len(vs_parks) > 0 and traSMAPy.step > 10:
            try:
                if not vs_parks[0][0].isPending(): # very expensive
                    vs_parks[0][0].stopFor(vs_parks[0][1], random.randint(400, 600), 
                                               stopParams=[StopType.PARKING])
                    vs_parks.pop(0)
            except Exception as e:
                print(e)
                vs_parks.pop(0)
                pass
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("sim.sumocfg")
    run(traSMAPy)
