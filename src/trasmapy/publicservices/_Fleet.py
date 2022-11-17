from typing_extensions import override

from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy._SimUpdatable import SimUpdatable
from trasmapy.publicservices._FleetStop import FleetStop
from trasmapy.users._Route import Route
from trasmapy.users._Users import Users
from trasmapy.users._Vehicle import Vehicle
from trasmapy.users._VehicleType import VehicleType


class Fleet(IdentifiedObject, SimUpdatable):
    def __init__(
        self,
        fleetId: str,
        fleetRoute: Route,
        vehicleType: VehicleType,
        fleetStops: list[FleetStop],
        end: float,
        period: int,
        start: float = 0,
    ) -> None:
        super().__init__(fleetId)
        self._route = fleetRoute
        self._vehicleType = vehicleType
        self._fleetStops = fleetStops
        self._end = end
        self._period = period
        self._start = start

        self._lastSpawn: float = -1.0
        self._nextSpawn: float = -1.0
        self._spawnedVehiclesIds: list[str] = []
        self._vehicles: list[Vehicle] = []

    @property
    def vehicleType(self) -> VehicleType:
        return self._vehicleType

    @property
    def route(self) -> Route:
        return self._route

    @property
    def fleetStops(self) -> list[FleetStop]:
        return self._fleetStops.copy()

    @property
    def end(self) -> float:
        return self._end

    @property
    def period(self) -> float:
        return self._period

    @property
    def start(self) -> float:
        return self._start

    @property
    def lastSpawnTime(self) -> float:
        """Last spawn vehicle simulation time.
        -1 means no spawn yet."""
        return self._lastSpawn

    @property
    def nextSpawnTime(self) -> float:
        """Simulation time of the next vehicle spawn.
        Note that due to update rates, the spawn might occur later than this time.
        -1 means first spawn."""
        return self._lastSpawn

    @property
    def spawnedVehiclesIds(self) -> list[str]:
        """Ids of all vehicles spawned until the current simulation step."""
        return self._spawnedVehiclesIds.copy()

    @property
    def vehicles(self) -> list[Vehicle]:
        """The vehicles that are currently present in the simulation."""
        return self._vehicles.copy()

    @override
    def _doSimulationStep(self, *args, step: int, time: float) -> None:
        users = args[0]
        if self._start < time < self._end and self._nextSpawn <= time:
            self._spawnVehicle(users)
            self._lastSpawn = time
            self._nextSpawn += self._period
        # remove dead vehicles from the list
        self._vehicles = list(filter(lambda v: not v.isDead(), self._vehicles))

    def _spawnVehicle(self, users: Users):
        newVehicleId: str = f"fleet{self.id}{len(self._spawnedVehiclesIds)}"
        self._spawnedVehiclesIds.append(newVehicleId)

        newVehicle = users.createVehicle(
            newVehicleId, route=self._route, vehicleType=self._vehicleType
        )
        for fleetStop in self._fleetStops:
            stop = fleetStop.stop
            newVehicle.stop(
                stop,
                duration=fleetStop.duration,
                until=fleetStop.until,
            )
        self._vehicles.append(newVehicle)
