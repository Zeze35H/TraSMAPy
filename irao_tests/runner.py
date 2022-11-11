#!/usr/bin/env python


from TraSMAPy import TraSMAPy


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    traSMAPy.startSimulation()

    traSMAPy.vehicle.add("vehicle0", "route0")
    while traSMAPy.simulation.getMinExpectedNumber() > 0:
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy()
    run(traSMAPy)
