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

    # vehicle types
    defaultVehicle = traSMAPy.users.getVehicleType("DEFAULT_VEHTYPE")
    evehicleType = defaultVehicle.duplicate("evehicle")
    evehicleType.vehicleClass = VehicleClass.EVEHICLE
    evehicleType.color = Color(100, 100, 255)

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

    PARKING_AREAS = [traSMAPy.network.getStop(f'pa_{x}') for x in range(7)]
    
    # setup custom route
    ROUTES = [
        create_route("r_north_south", [e40, e9], prob=0.6),
        # create_route("pa_north", [e40, e40r], r_type="parking", prob=0.10, parks=PARKING_AREAS[:4]),
        create_route("pa_south", [e6, e6r], r_type="parking", prob=0.40, parks=PARKING_AREAS)
    ]
    # TODO fix conflicting park routes
    # TODO semaphores
    
    V_TYPES = [defaultVehicle, evehicleType]
    
    ROUTE_PROBS = [x["prob"] for x in ROUTES]
    if None in ROUTE_PROBS or sum(ROUTE_PROBS) != 1:
        ROUTE_PROBS = None
        print("Ignoring route probalities.")
        
    vs_parks = []
    for i in range(0, 1000):
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
                if not vs_parks[0][0].isPending():
                    vs_parks[0][0].stopFor(vs_parks[0][1], random.randint(400, 600), 
                                               stopParams=[StopType.PARKING])
                    vs_parks.pop(0)
            except Exception as e:
                print(e)
                pass
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("sim.sumocfg")
    run(traSMAPy)
