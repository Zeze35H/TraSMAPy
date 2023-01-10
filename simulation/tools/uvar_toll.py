from collections import defaultdict
from trasmapy import Toll
from trasmapy.network._Detector import Detector
from trasmapy import TraSMAPy
import random

class UVAR_Toll(Toll):

    def __init__(self, id: str, detect_price: list[dict[list, float]], 
                 price : float, ctx : TraSMAPy) -> None:

        
        self.price = price
        self._hist_step = 0
        self._toll_hist = defaultdict(lambda: 0.0)
        self._ctx = ctx

        self.detect_prices = detect_price

        detectors = []
        for det_price in detect_price:
            for detector in det_price["detectors"]:
                # add effort to edge containing toll (vehicles try to avoid if possible)
                toll_edge = self._ctx.network.getLane(detector.laneId).parentEdge
                toll_edge.setEffort(toll_edge.travelTime * (1 + det_price["price"]))
                detectors.append(detector)

            print(toll_edge.travelTime)
            print(toll_edge.getEffort(0))
        
        super().__init__(id, detectors)

    def recalculate_efforts(self):
        """The edge efforts need to be recalculated ate every step because of the dynamic random weights applied to travel time.
           Vehicles will be more likely to choose alternative routes during runtime.
        """

        for det_price in self.detect_prices:
            for detector in det_price["detectors"]:
                # add effort to edge containing toll (vehicles try to avoid if possible)
                toll_edge = self._ctx.network.getLane(detector.laneId).parentEdge
                toll_edge.setEffort((toll_edge.travelTime * (1 + det_price["price"])))
        
    def roadPricingScheme(self, detectedVehicles):
        self._toll_hist[self._ctx.step] = self.price * len(detectedVehicles)

    @property
    def toll_hist(self):
        return self._toll_hist