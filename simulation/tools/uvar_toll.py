from collections import defaultdict
from trasmapy import Toll
from trasmapy.network._Detector import Detector
from trasmapy import TraSMAPy

class UVAR_Toll(Toll):

    def __init__(self, id: str, detectors: list[Detector], 
                 price : float, ctx : TraSMAPy, effort : float = 300) -> None:
        super().__init__(id, detectors)
        
        self.price = price
        self._hist_step = 0
        self._toll_hist = defaultdict(lambda: 0.0)
        self._ctx = ctx

        # add effort to edge containing toll (vehicles try to avoid if possible)
        toll_edge = self._ctx.network.getLane(detectors[0].laneId).parentEdge
        toll_edge.setEffort(toll_edge.travelTime + effort)
        
    def roadPricingScheme(self, detectedVehicles):
        self._toll_hist[self._ctx.step] = self.price * len(detectedVehicles)

    @property
    def toll_hist(self):
        return self._toll_hist