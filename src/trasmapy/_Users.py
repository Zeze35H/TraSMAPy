import traci
from traci.constants import VAR_STOPSTATE

from trasmapy.users._Vehicle import Vehicle


class Users:
    def __init__(self):
        # the vehicles being tracked
        self._vehicles: dict[str, Vehicle] = {}

    def getAllVehicleIds(self) -> list[str]:
        return traci.vehicle.getIDList()  # type: ignore

    def getAllPendingVehicleIds(self) -> list[str]:
        return traci.simulation.getPendingVehicles()  # type: ignore

    def getAllVehicleTypeIds(self) -> list[str]:
        return traci.vehicletype.getIDList()  # type: ignore

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
        routeId: str,
        typeId: str = "DEFAULT_VEHTYPE",
        personNumber: int = 0,
        personCapacity: int = 0,
    ) -> Vehicle:
        """Creates a vehicle and adds it to the network.
        If the route is empty (\"\"), the vehicle will be added to a random network edge.
        If the route consists of two disconnected edges, the vehicle will be treated like
        a <trip> and use the fastest route between the two edges."""
        try:
            traci.vehicle.add(
                vehicleId,
                routeId,
                typeID=typeId,
                personNumber=personNumber,
                personCapacity=personCapacity,
            )
            return self._registerVehicle(vehicleId)
        except traci.TraCIException as e:
            raise KeyError(
                f"A error occured while adding the vehicle with the given ID: [vehicleId={vehicleId}], [error={e}]."
            )

    def _registerVehicle(self, vehicleId) -> Vehicle:
        # subscribe stoped state byte (check liveness)
        traci.vehicle.subscribe(vehicleId, [VAR_STOPSTATE])

        v = Vehicle(vehicleId)
        self._vehicles[vehicleId] = v
        return v

    def _doSimulationStep(self) -> None:
        res: dict[str, dict] = traci.vehicle.getAllSubscriptionResults()  # type: ignore
        # the vehicles that exited the simulation on this step
        vehiclesThatDied: set[str] = self._vehicles.keys() - res.keys()

        for vehicleId in vehiclesThatDied:
            # garanteed to be in the map (doesn't need catch)
            v = self._vehicles.pop(vehicleId)
            v._dead = True
