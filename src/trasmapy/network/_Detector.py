from typing_extensions import override
import traci

from trasmapy._SimUpdatable import SimUpdatable
from trasmapy._IdentifiedObject import IdentifiedObject


class Detector(IdentifiedObject, SimUpdatable):
    def __init__(self, detectorId: str) -> None:
        super().__init__(detectorId)
        self._listeners = []

    @property
    def timeSinceLastDetection(self) -> float:
        """Returns how many seconds elapsed since the last detection."""
        return traci.inductionloop.getTimeSinceDetection(self.id)  # type: ignore

    @property
    def laneId(self) -> str:
        """Returns the ID of the lane where the detector is placed."""
        return traci.inductionloop.getLaneID(self.id)  # type: ignore

    @property
    def position(self) -> float:
        """Returns the position of the detection on its containing lane."""
        return traci.inductionloop.getPosition(self.id)  # type: ignore

    def listen(self, listener):
        """Hooks into the detector. The given function will be called with the IDs of the detected vehicles there's a detection."""
        self._listeners.append(listener)

    @override
    def _doSimulationStep(self, *args, step: int, time: float) -> None:
        # detectedVehicles = traci.inductionloop.getLastStepVehicleIDs(self.id)
        detected = traci.inductionloop.getVehicleData(self.id)
        if len(detected) == 0:
            # nothing happened
            return

        for listener in self._listeners:
            listener(detected)
