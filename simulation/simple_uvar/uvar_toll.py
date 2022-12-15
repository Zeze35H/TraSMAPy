from trasmapy import Toll
from trasmapy.network._Detector import Detector

class UVAR_Toll(Toll):

    def __init__(self, id: str, detectors: list[Detector], 
                 vtype_prices : dict[str, float]) -> None:
        super().__init__(id, detectors)
        
        if not vtype_prices:
            raise TypeError("missing vtype_prices.")
        
        self.vtype_prices = vtype_prices
        self.detected = set()
        self._hist_step = 0
        self._toll_hist = {}
        
    def roadPricingScheme(self, detectedVehicles):
        for v in detectedVehicles:
            self.detected.add(v)