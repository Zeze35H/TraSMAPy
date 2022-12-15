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
    
    # Detectors
    # traSMAPy.network.getDetector("e")
    sw_in0 = traSMAPy.network.getDetector("sw_in0")
    sw_in1 = traSMAPy.network.getDetector("sw_in1")
    
    sw_out0 = traSMAPy.network.getDetector("sw_out0")
    sw_out1 = traSMAPy.network.getDetector("sw_out1")

    queryStr = "network/edges[self.id == 'E40']/vehicleCount"
    traSMAPy.registerQuery("north_in_ve_count", queryStr)
    
    traSMAPy.registerQuery("north_emissions", "network/edges[self.id == 'E40']/CO2Emissions")
    
    # traSMAPy.users.vehicleTypes.length    
    traSMAPy.registerQuery("active_cars", "users/vehicles")
    # # main_det = traSMAPy.network.getDetector("main_detector")
    # traSMAPy.users.vehicles.
    # print(main_det.__dict__)
    
    def process_in(x):
        for v in x:
            vehicle = traSMAPy.users.getVehicle(v)
            # print(vehicle)
            # print(dir(vehicle))
            # print(vehicle.__dict__)
    
    sw_in0.listen(process_in)


    PARKING_AREAS_SOUTH = [traSMAPy.network.getStop(f'pa_sw{x}') for x in range(7)]

    V_TYPES = [defaultVehicle, evehicleType]
    
    # setup custom routes
    ROUTES = [
        create_route("r_north_south", [e40, e9], prob=0.6), # NW-SE
        create_route("pa_south", [e6, e6r], r_type="parking", prob=0.4, parks=PARKING_AREAS_SOUTH) # SW-SW
    ]
    
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
    
    vs_parks = []
    for i in range(0, 800):
        route = random.choices(ROUTES, weights=ROUTE_PROBS, k=1)[0]
        
        v = traSMAPy.users.createVehicle(f"v{i}", route["route"], 
                                            random.choices(V_TYPES, weights=(80, 20), k=1)[0])
        if route["type"] == "parking":
            park = random.choice(route["park_areas"])
            v.via = [park.lane.parentEdge.id]
            vs_parks.append((v, park))
    
    spawned = False
    while traSMAPy.minExpectedNumber > 0: 
        try:
            if len(vs_parks) > 0:
                if spawned:
                    spawned = False
                    vs_parks[0][0].stopFor(vs_parks[0][1], random.randint(400, 600), 
                                                    stopParams=[StopType.PARKING, StopType.PARKING_AREA])
                    vs_parks.pop(0)
                    continue
                
                spawned = not vs_parks[0][0].isPending()
        except Exception as e:
            print(e)
            pass
        traSMAPy.doSimulationStep()
    
    # traSMAPy.users.vehicles.count
    print(traSMAPy.collectedStatistics[100])
    # print(traSMAPy.query(queryStr))
    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("sim.sumocfg")
    run(traSMAPy)
