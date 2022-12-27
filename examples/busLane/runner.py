#!/usr/bin/env python

from random import random
from trasmapy import TraSMAPy, VehicleClass, Color


def run(traSMAPy: TraSMAPy):
    # reserve lane to buses
    lane = traSMAPy.network.getLane("E2_0")
    lane.setAllowed([VehicleClass.BUS])

    # create bus vehicle type
    default_vtype = traSMAPy.users.getVehicleType("DEFAULT_VEHTYPE")
    bus_vtype = default_vtype.duplicate("BUS_VEHTYPE")
    bus_vtype.vehicleClass = VehicleClass.BUS
    bus_vtype.color = Color(255, 0, 255)

    bus_change = 0.25
    i = 0

    traSMAPy.users.createVehicle(
        f"b{i}", vehicleType=bus_vtype if random() <= bus_change else default_vtype
    )

    """execute the TraCI control loop"""
    while traSMAPy.minExpectedNumber > 0:
        i += 1
        traSMAPy.users.createVehicle(
            f"b{i}", vehicleType=bus_vtype if random() <= bus_change else default_vtype
        )

        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("config.sumocfg")
    run(traSMAPy)
