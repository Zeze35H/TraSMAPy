from trasmapy import Toll
from trasmapy.network._Detector import Detector
from trasmapy import TraSMAPy

class UVAR_Toll(Toll):

    def __init__(self, id: str, detectors: list[Detector], 
                 vtype_prices : dict[str, float], ctx : TraSMAPy, effort : float = 300) -> None:
        super().__init__(id, detectors)
        
        if not vtype_prices:
            raise TypeError("missing vtype_prices.")
        
        self.vtype_prices = vtype_prices
        self._hist_step = 0
        self._toll_hist = {}
        self._ctx = ctx

        # add effort to edge containing toll (vehicles try to avoid if possible)
        toll_edge = self._ctx.network.getLane(detectors[0].laneId).parentEdge
        toll_edge.setEffort(0, 100000, effort)
        
    def roadPricingScheme(self, detectedVehicles):
        self._toll_hist[self._ctx.step] = self._toll_hist.get(self._ctx.step, 0)
        for v in detectedVehicles:
            self._toll_hist[self._ctx.step] += self.vtype_prices[v[4]]        

    @property
    def toll_hist(self):
        return self._toll_hist