#!/usr/bin/env python


from trasmapy import TraSMAPy, Color, VehicleClass, StopType



def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""


    # vehicle types
    defaultVehicle = traSMAPy.users.getVehicleType("DEFAULT_VEHTYPE")
    evehicleType = defaultVehicle.duplicate("evehicle")
    evehicleType.vehicleClass = VehicleClass.EVEHICLE
    evehicleType.color = Color(0, 0, 255)

    # get edges
    e40 = traSMAPy.network.getEdge("E40")
    e9 = traSMAPy.network.getEdge("E9")

    e53 = traSMAPy.network.getEdge("E53")
    e58 = traSMAPy.network.getEdge("E58")
    e48 = traSMAPy.network.getEdge("E48")
    
    e41 = traSMAPy.network.getEdge("E41")
    e41a = traSMAPy.network.getEdge("-E41.28")


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

    stop0 = traSMAPy.network.createEdgeStop(edgeId=e31.id, startPos=10, endPos=10)
    # lane0 = e53.getLane("E31_0")
    # stop0 = traSMAPy.network.createLaneStop(lane0.id, endPos=0)

    pa_0 = traSMAPy.network.getStop('pa_0')

    # v = traSMAPy.users.createVehicle(f"vehicle1", route2, defaultVehicle)
    
    vs = []
    evs = []
    for i in range(0, 300, 3):
        # traSMAPy.users.createVehicle(f"vehicle{i}", route0, defaultVehicle)
        vs.append(traSMAPy.users.createVehicle(f"vehicle{i+1}", route2, defaultVehicle))
        evs.append(traSMAPy.users.createVehicle(f"vehicle{i+2}", route2, evehicleType))

        
    while traSMAPy.minExpectedNumber > 0:

        # if traSMAPy.step == 10:
        #     v.stopFor(stop0, 0.1)

        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("sim.sumocfg")
    run(traSMAPy)
