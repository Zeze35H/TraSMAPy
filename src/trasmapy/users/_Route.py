import traci

from trasmapy._IdentifiedObject import IdentifiedObject


class Route(IdentifiedObject):
    def __init__(self, routeId: str) -> None:
        super().__init__(routeId)

    @property
    def edgesIds(self) -> list[str]:
        return traci.route.getEdges(self.idself.id)  # type: ignore
