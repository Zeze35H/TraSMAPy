from abc import abstractmethod

from trasmapy.network._Detector import Detector
from trasmapy._IdentifiedObject import IdentifiedObject


class Toll(IdentifiedObject):
    def __init__(self, id: str, detectors: list[Detector]) -> None:
        super().__init__(id)
        self._detectors = detectors
        for detector in self._detectors:
            detector.listen(self.roadPricingScheme)

    @property
    def detectors(self) -> list[Detector]:
        return self._detectors

    @abstractmethod
    def roadPricingScheme(self, detectedVehicles):
        pass
