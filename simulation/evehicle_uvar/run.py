#!/usr/bin/env python
from typing import Any, Dict
import argparse
import random

import sys
sys.path.append("..")
from tools.trasmapy_utils import *

from trasmapy import TraSMAPy
from trasmapy import StopType

def run(context: TraSMAPy, opt: Dict[str, Any]):
    # Vehicle Types
    default_vehicle = get_default_vtype(context)
    electric_vehicle = get_electric_vtype(context)

    # Edges
    north_edge = context.network.getEdge("E40")
    north_edge_rev = context.network.getEdge("-E40")
    
    entrance_edge = context.network.getEdge("E41")
    entrance_edge_rev = context.network.getEdge("-E41.28")

    southeast_edge = context.network.getEdge("E19.70")
    southwest_edge = context.network.getEdge("E6")
    southwest_edge_rev = context.network.getEdge("-E6")

    # Forbid Edges
    if opt["forbid"]:
        entrance_edge.setDisallowed([default_vehicle.vehicleClass])
        entrance_edge_rev.setDisallowed([default_vehicle.vehicleClass])

    # Data collection
    edges_idx = {edge.id : idx for idx, edge in enumerate(context.network.edges)}

    ## Total vehicles on city
    context.registerQuery("active_vehicles",
        lambda ctx: len(ctx["users"].vehicles)
    )

    ## C02 Emission on city interior
    edges_co2_tocollect = [
        "E0", "E1", "E2", "E3", "E4",
        "E50", "-E50.40", "E49", "-E49",
        "E10", "-E110", "E10.256", "-E100",
        "E470", "-E47", "E420", "-E42",
        "E43", "-E43", "E44", "-E44",
        "E45", "-E45", "E46", "-E46.33",
        "E510", "-E51", "E52", "-E52",
        "E56", "-E560", "E55", "-E55",
        "E5", "-E5", "-E27", "E54", "-E54",
        "E53", "-E53", "E58",
        "E14", "E15", "E16", "E17"

    ]
    context.registerQuery("city_co2",
        lambda ctx: sum([
            ctx["network"].edges[edges_idx[idx]].CO2Emissions
                for idx in edges_co2_tocollect
        ])
    )

    # Routes
    routes = [
        create_trip(context, "north_south", [north_edge, southeast_edge], weight=0.4),
        create_trip(context, "north_north", [north_edge, north_edge_rev], weight=0.3),
        create_trip(context, "south_south", [southwest_edge, southwest_edge_rev], weight=0.3),
    ]

    route_weights = [route.get("weight", 0.5) for route in routes]

    edge_stops = ["E5", "E52", "E54", "-E53", "E53", "E5", "-E5", "E44", "-E44", "E43", "-E43", "-E42", "E420"]


    edge_stops = [context.network.getEdge(x) for x in edge_stops]
    lane_stops = [edge.lanes[0] for edge in edge_stops]
    lane_stops = [context.network.createLaneStop(lane.id, lane.length/2) for lane in lane_stops]

    # Generate Vehicles
    vs_stops = {}
    vehicle_types = [default_vehicle, electric_vehicle]
    for i in range(opt.get("no_vehicles", 2000)):
        vehicle_route = random.choices(
            routes,
            weights=route_weights
        )[0]

        v = context.users.createVehicle(
            f"v{i}", route=vehicle_route["route"],
            vehicleType=random.choices(vehicle_types, weights=(0.8, 0.2))[0],
            departTime=random.randint(0, 1000)
        )

        lane_stop = random.choices(lane_stops, k=1)[0]
        v.via = [lane_stop.lane.parentEdge.id]
        vs_stops[v.id] = lane_stop

    while context.minExpectedNumber > 0:
        for v in context.users.pendingVehicles:
            if v.id not in vs_stops: continue
            v.stopFor(vs_stops[v.id], duration=random.randint(400, 600), stopParams=[StopType.PARKING])

        context.doSimulationStep()

    context.closeSimulation()

def parse_opt():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--sumocfg", default="sim.sumocfg")
    parser.add_argument("--forbid", action="store_true", default=False)
    parser.add_argument("-n", "--no-vehicles",  type=int, default=2000)


    args = parser.parse_args()
    return vars(args)

if __name__ == "__main__":

    opt = parse_opt()

    context = TraSMAPy(opt["sumocfg"])

    run(context=context, opt=opt)