#!/usr/bin/env python
from typing import Any, Dict
import argparse
import random

from trasmapy_utils import create_trip, get_default_vtype, get_electric_vtype
from trasmapy import TraSMAPy

def run(context: TraSMAPy, opt: Dict[str, Any]):
    print("HERE")
    # Vehicle Types
    default_vehicle = get_default_vtype(context)
    electric_vehicle = get_electric_vtype(context)

    # Edges
    north_edge = context.network.getEdge("E40")
    north_edge_rev = context.network.getEdge("-E40")
    
    entrance_edge = context.network.getEdge("E41")
    entrance_edge_rev = context.network.getEdge("-E41.28")

    southeast_edge = context.network.getEdge("E19")
    southwest_edge = context.network.getEdge("E6")

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
            ctx["network"].edges[edges_idx[idx]].C02Emissions
                for idx in edges_co2_tocollect
        ])
    )

    # Routes
    routes = [
        create_trip(context, "north_south", [north_edge, southwest_edge], weight=0.5),
        create_trip(context, "south_north", [southeast_edge, north_edge_rev], weight=0.5)
    ]

    route_weights = [route.get("weight", 0.5) for route in routes]

    # Generate Vehicles
    vehicle_types = [default_vehicle, electric_vehicle]
    for i in range(opt.get("no_vehicles", 800)):
        vehicle_route = random.choices(
            routes,
            weights=route_weights
        )[0]

        context.users.createVehicle(
            f"v{i}", route=vehicle_route["route"],
            vehicleType=random.choices(vehicle_types, weights=(0.8, 0.2))[0]
        )

    while context.minExpectedNumber > 0:
        context.doSimulationStep()

    context.closeSimulation()

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sumocfg", default="sim.sumocfg")
    parser.add_argument("--forbid", action="store_true", default=False)
    parser.add_argument("--no-vehicles", type=int, default=800)

    args = parser.parse_args()
    return vars(args)

if __name__ == "__main__":
    opt = parse_opt()

    context = TraSMAPy(opt["sumocfg"])

    run(context=context, opt=opt)