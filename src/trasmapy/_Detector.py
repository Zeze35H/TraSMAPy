import traci

from trasmapy._IdentifiedObject import IdentifiedObject

class Detector(IdentifiedObject):
    def __init__(self, detectorId: str) -> None:
        super().__init__(detectorId)
        self._listeners = []

    def listen(self, listener):
        """Hooks into the detector. The given function will be called with the IDs of the detected vehicles there's a detection."""
        self._listeners.append(listener)

    def _doSimulationStep(self):
        if traci.inductionloop.getLastStepVehicleNumber(self.id) == 0:
            # nothing happened
            return

        detectedVehicles = traci.inductionloop.getLastStepVehicleIDs(self.id)
        for listener in self._listeners:
            listener(detectedVehicles)
