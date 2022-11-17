#!/usr/bin/env python


from trasmapy import TraSMAPy, VehicleClass, StopType, ScheduledStop

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    while traSMAPy.minExpectedNumber > 0:
        traSMAPy.doSimulationStep()

    #  print(traSMAPy.collectedStatistics)
    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("osm.sumocfg")
    run(traSMAPy)
