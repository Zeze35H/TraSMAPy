#!/usr/bin/env python


from trasmapy import TraSMAPy, Color, VehicleClass



def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    
    e40 = traSMAPy.network.getEdge("E40")
    e53 = traSMAPy.network.getEdge("E53")
    e48 = traSMAPy.network.getEdge("E48")
    
    
    e41 = traSMAPy.network.getEdge("E41")
    defaultVehicle = traSMAPy.users.getVehicleType("DEFAULT_VEHTYPE")
    
    evehicleType = defaultVehicle.duplicate("evehicle")
    evehicleType.vehicleClass = VehicleClass.EVEHICLE
    evehicleType.color = Color(0, 0, 255)
    e41.setDisallowed([defaultVehicle.vehicleClass])
        
    route0 = traSMAPy.users.getRoute('r_0')    
    
    route1 = traSMAPy.users.createRouteFromEdges("r_2", [e40, e53, e48])

    for i in range(0, 300, 3):
        traSMAPy.users.createVehicle(f"vehicle{i}", route0, defaultVehicle)
        traSMAPy.users.createVehicle(f"vehicle{i+1}", route1, defaultVehicle)
        traSMAPy.users.createVehicle(f"vehicle{i+2}", route1, evehicleType)
        
    while traSMAPy.minExpectedNumber > 0:
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("sim.sumocfg")
    run(traSMAPy)
