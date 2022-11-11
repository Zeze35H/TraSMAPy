import os
import sys
import optparse

# we need to import python modules from the $SUMO_HOME/tools directory
if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

from trasmapy.Concessioner import Concessioner

class TraSMAPy:
    def __init__(self, sumoCfg: str) -> None:
        self._step: int = 0
        self._startSimulation(sumoCfg)
        self._concessioner = Concessioner()

    @property
    def step(self) -> int:
        return self._step

    @property
    def concenssioner(self) -> Concessioner:
        return self._concessioner

    def closeSimulation(self) -> None:
        traci.close()
        sys.stdout.flush()

    def doSimulationStep(self) -> None:
        self._step += 1
        traci.simulationStep()
        self._concessioner._doSimulationStep()

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
        traci.start(
            [sumoBinary, "-c", sumoCfg, "--tripinfo-output", "tripinfo.xml"]
        )
