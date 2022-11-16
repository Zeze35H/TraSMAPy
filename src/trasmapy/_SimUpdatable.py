from abc import abstractmethod


class SimUpdatable:
    @abstractmethod
    def _doSimulationStep(self, *args, step: int, time: float) -> None:
        pass
