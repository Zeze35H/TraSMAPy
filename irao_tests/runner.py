#!/usr/bin/env python


from trasmapy import TraSMAPy

import traci


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    traSMAPy.vehicle.add("vehicle0", "route0")

    while traSMAPy.simulation.getMinExpectedNumber() > 0:
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy()
    run(traSMAPy)
