from abc import abstractmethod

from trasmapy.color.Color import Color


class Colorable:
    @property
    @abstractmethod
    def color(self) -> Color:
        pass

    @color.setter
    @abstractmethod
    def color(self, color: Color) -> None:
        pass
