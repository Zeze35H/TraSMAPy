Quickstart with TraSMAPy
========================

After installing TraSMAPy, you need a network to work with. The `netgenerate`
utility from SUMO can be used to generate a simple network. The following
command will generate a random network:

    netgenerate --rand -o rand.net.xml

The file `rand.net.xml` containes our network. Now we need a sumo configuration
file to run the simulation. You can put the following in the a `rand.sumocfg` file:

.. code-block::

    <configuration>
        <input>
            <net-file value="rand.net.xml"/>
        </input>
    </configuration>

Note that you can also consult the `official SUMO documentation <https://sumo.dlr.de/docs/index.html#network_building>`_
for more information about importing, building, and customizing networks.

With this, we are ready to write our runner script and use TraSMAPy. Create a `runner.py`
file with the following content:

.. code-block::

    #!/usr/bin/env python

    from trasmapy import TraSMAPy

    def run(traSMAPy: TraSMAPy):
        """execute the TraCI control loop"""
        while traSMAPy.minExpectedNumber > 0:
            traSMAPy.doSimulationStep()

        traSMAPy.closeSimulation()


    if __name__ == "__main__":
        traSMAPy = TraSMAPy("rand.sumocfg")
        run(traSMAPy)

