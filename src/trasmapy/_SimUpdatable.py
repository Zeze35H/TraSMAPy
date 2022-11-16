from abc import abstractmethod


class SimUpdatable:
    @abstractmethod
    def _doSimulationStep(self, step: int, time: float):
        pass
