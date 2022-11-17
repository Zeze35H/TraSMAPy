from typing import Union
from typing_extensions import override

import traci
from traci.constants import VAR_STOPSTATE

from trasmapy._SimUpdatable import SimUpdatable
from trasmapy.users._Vehicle import Vehicle
from trasmapy.users._VehicleType import VehicleType
from trasmapy.users._Route import Route
from trasmapy.network._Edge import Edge


class Users(SimUpdatable):
    def __init__(self):
        # the vehicles being tracked
        self._vehicles: dict[str, Vehicle] = {}

    def getAllVehicleIds(self) -> list[str]:
        return traci.vehicle.getIDList()  # type: ignore

    def getAllPendingVehicleIds(self) -> list[str]:
        return traci.simulation.getPendingVehicles()  # type: ignore

    def getAllVehicleTypeIds(self) -> list[str]:
        return traci.vehicletype.getIDList()  # type: ignore

    def getVehicleType(self, vehicleTypeId: str) -> VehicleType:
        if vehicleTypeId not in self.getAllVehicleTypeIds():
            raise KeyError(
                f"The vehicle type with the given ID does not exist: [vehicleTypeId={vehicleTypeId}]."
            )
        return VehicleType(vehicleTypeId)

    def getVehicle(self, vehicleId: str) -> Vehicle:
        try:
            return self._vehicles[vehicleId]
        except KeyError:
            if (
                vehicleId in self.getAllVehicleIds()
                or vehicleId in self.getAllPendingVehicleIds()
            ):
                return self._registerVehicle(vehicleId)
            raise KeyError(
                f"There are no vehicles with the given ID in the simulation: [vehicleId={vehicleId}]"
            )

    def createVehicle(
        self,
        vehicleId: str,
        route: Union[Route, None] = None,
        vehicleType: VehicleType = VehicleType("DEFAULT_VEHTYPE"),
        personNumber: int = 0,
        personCapacity: int = 0,
    ) -> Vehicle:
        """Creates a vehicle and adds it to the network.
        If the route is None, the vehicle will be added to a random network edge.
        If the route consists of two disconnected edges, the vehicle will be treated like
        a <trip> and use the fastest route between the two edges."""
        try:
            traci.vehicle.add(
                vehicleId,
                route.id if isinstance(route, Route) else "",
                typeID=vehicleType.id,
                personNumber=personNumber,
                personCapacity=personCapacity,
            )
            return self._registerVehicle(vehicleId)
        except traci.TraCIException as e:
            raise KeyError(
                f"A error occured while adding the vehicle with the given ID: [vehicleId={vehicleId}], [error={e}]."
            )

    def getRoute(self, routeId: str) -> Route:
        if routeId not in traci.route.getIDList():
            raise KeyError(
                f"The given route ID doesn't belong to any registered route: [routeId={routeId}]"
            )
        return Route(routeId)

    def createRouteFromIds(self, routeId: str, edgesIds: list[str]) -> Route:
        try:
            traci.route.add(routeId, edgesIds)
        except traci.TraCIException as e:
            raise KeyError(
                f"A error occured while adding the route with the given ID: [vehicleId={routeId}], [error={e}]."
            )
        return Route(routeId)

    def createRouteFromEdges(self, routeId: str, edges: list[Edge]) -> Route:
        return self.createRouteFromIds(routeId, list(map(lambda x: x.id, edges)))

    def _registerVehicle(self, vehicleId) -> Vehicle:
        # subscribe stoped state byte (check liveness)
        traci.vehicle.subscribe(vehicleId, [VAR_STOPSTATE])

        v = Vehicle(vehicleId)
        self._vehicles[vehicleId] = v
        return v

    @override
    def _doSimulationStep(self, *args, step: int, time: float) -> None:
        res: dict[str, dict] = traci.vehicle.getAllSubscriptionResults()  # type: ignore
        # the vehicles that exited the simulation on this step
        vehiclesThatDied: set[str] = self._vehicles.keys() - res.keys()

        for vehicleId in vehiclesThatDied:
            # garanteed to be in the map (doesn't need catch)
            v = self._vehicles.pop(vehicleId)
            v._dead = True
