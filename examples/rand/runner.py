#!/usr/bin/env python


from trasmapy import TraSMAPy


def run(traSMAPy: TraSMAPy):
    """execute the TraCI control loop"""
    for i in range(0, 50):
        traSMAPy.users.createVehicle(f"vehicle{i}", None)

    while traSMAPy.minExpectedNumber > 0:
        traSMAPy.doSimulationStep()

    traSMAPy.closeSimulation()


if __name__ == "__main__":
    traSMAPy = TraSMAPy("rand.sumocfg")
    run(traSMAPy)
