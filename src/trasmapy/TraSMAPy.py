import os
import sys
import optparse

# we need to import python modules from the $SUMO_HOME/tools directory
if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    exit("Please declare environment variable 'SUMO_HOME'.")

from sumolib import checkBinary
import traci
import pyflwor

from trasmapy.network._Network import Network
from trasmapy.users._Users import Users
from trasmapy.publicservices._PublicServices import PublicServices


class TraSMAPy:
    def __init__(self, sumoCfg: str) -> None:
        self._step: int = 0
        self._collectedStatistics: dict[int, dict] = {}
        self._queries = {}

        self._startSimulation(sumoCfg)
        self._network: Network = Network()
        self._users: Users = Users()
        self._publicServices: PublicServices = PublicServices()

    @property
    def network(self) -> Network:
        return self._network

    @property
    def users(self) -> Users:
        return self._users

    @property
    def publicServices(self) -> PublicServices:
        return self._publicServices

    @property
    def step(self) -> int:
        return self._step

    @property
    def stepLength(self) -> float:
        """The length of one simulation step (s)."""
        return traci.simulation.getDeltaT()  # type: ignore

    @property
    def timeMs(self) -> float:
        """The current simulation time (ms)."""
        return traci.simulation.getCurrentTime()  # type: ignore

    @property
    def time(self) -> float:
        """The current simulation time (s)."""
        return traci.simulation.getTime()  # type: ignore

    @property
    def minExpectedNumber(self) -> int:
        return traci.simulation.getMinExpectedNumber()  # type: ignore

    @property
    def collectedStatistics(self) -> dict[int, dict]:
        """The accumulated statistics of the queries."""
        return self._collectedStatistics.copy()

    def query(self, queryString: str) -> dict:
        """Run a query once and get its current result."""
        return pyflwor.execute(
            queryString,
            {
                "network": self._network,
                "users": self._users,
                "publicServices": self._publicServices,
            },
        )

    def registerQuery(self, queryName: str, queryString: str) -> None:
        """Register query to be run every tick.
        Results are accumulated and can be obtained through the collectedStatistics property."""
        if queryName in self._queries:
            raise KeyError(
                f"There's a query with that name already registered: [queryName={queryName}]."
            )
        self._queries[queryName] = pyflwor.compile(queryString)

    def doSimulationStep(self) -> None:
        self._step += 1
        traci.simulationStep()

        time = self.time
        self._network._doSimulationStep(self._step, time)
        self._users._doSimulationStep(self._step, time)
        self._publicServices._doSimulationStep(self._step, time)

        self._collectedStatistics[self._step] = {}
        for query in self._queries.items():
            self._collectedStatistics[self._step][query[0]] = query[1](
                {
                    "network": self._network,
                    "users": self._users,
                    "publicServices": self._publicServices,
                }
            )

    def closeSimulation(self) -> None:
        traci.close()
        sys.stdout.flush()

    def _getOptions(self):
        optParser = optparse.OptionParser()
        optParser.add_option(
            "--nogui",
            action="store_true",
            default=False,
            help="run the commandline version of sumo",
        )
        options, args = optParser.parse_args()
        return options

    def _startSimulation(self, sumoCfg: str) -> None:
        options = self._getOptions()

        # script has been called from the command line. It will start sumo as a
        # server, then connect and run
        if options.nogui:
            sumoBinary = checkBinary("sumo")
        else:
            sumoBinary = checkBinary("sumo-gui")

        # sumo is started as a subprocess and then the python script connects and runs
        traci.start([sumoBinary, "-c", sumoCfg, "--tripinfo-output", "tripinfo.xml"])
