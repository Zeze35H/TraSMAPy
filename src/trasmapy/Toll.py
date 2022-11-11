from abc import abstractmethod

from trasmapy._Detector import Detector

class Toll():
    def __init__(self, detector) -> None:
        self._detector = detector

        self._detector.listen(self.roadPricingScheme)

    @property
    def detector(self) -> Detector:
        return self._detector

    @abstractmethod
    def roadPricingScheme(self, detectedVehicles):
        pass
