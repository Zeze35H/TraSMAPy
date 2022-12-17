Quickstart with TraSMAPy
========================

Generating our first network
----------------------------

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

Using TraSMAPy for the first time
---------------------------------

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

Running this python script will open the sumo-gui. You'll notice that if you start the
simulation (by pressing the play button), the simulation will end immediately. This is
because we have not added any vehicles to the simulation and are we only ticking the
simulation until there are no vehicles.

Adding vehicles to the simulation
---------------------------------

We can add vehicles to the simulation by chaging our `runner.py` file like so:
    
.. code-block::

    def run(traSMAPy: TraSMAPy):
        for i in range(100):
            traSMAPy.users.createVehicle(f"v{i}")

        """execute the TraCI control loop"""
        while traSMAPy.minExpectedNumber > 0:
            traSMAPy.doSimulationStep()

        traSMAPy.closeSimulation()

This will spawn 100 vehicles in the simulation. If you run the simulation again, you'll
notice that the vehicles will move around the network. You can also use the TraSMAPy
API to control the vehicles. For example, you can change the speed of all vehicles
like so:

.. code-block::

    def run(traSMAPy: TraSMAPy):
        for i in range(100):
            v = traSMAPy.users.createVehicle(f"v{i}")
            v.speed = 10

        """execute the TraCI control loop"""
        while traSMAPy.minExpectedNumber > 0:
            for vehicle in traSMAPy.users.getVehicles():
                vehicle.setSpeed(10)
            traSMAPy.doSimulationStep()

        traSMAPy.closeSimulation()

As you can see, vehicle, just like everything in TraSMAPy, are objects. This abstracts
away the complexity of the `TraCI API <https://sumo.dlr.de/docs/TraCI.html>`_ and makes
it easier to use.

Examining the network
---------------------

TraSMAPy also provides an API to examine the network. For example, you can get a sum
of all CO2Emissions in all edges in the network for each simulation tick like so:

.. code-block::

    def run(traSMAPy: TraSMAPy):
        """execute the TraCI control loop"""
        for i in range(100):
            v = traSMAPy.users.createVehicle(f"v{i}")
            v.speed = 10

        while traSMAPy.minExpectedNumber > 0:
            traSMAPy.doSimulationStep()

            edges = traSMAPy.network.edges
            co2Emissions = 0
            for edge in edges:
                co2Emissions += edge.CO2Emissions
            print(co2Emissions)

        traSMAPy.closeSimulation()

You'll probably notice that this makes the simulation run very slowly. This is because
you are iterating all network edges for each simulation tick.

Introduction to queries
-----------------------

TraSMAPy provides a query API to make it easier to query the network and aggregate
statistics. For this, there are two query mecanisms available: Python functions, and
the `Pyflwor query language <https://github.com/JoaoCostaIFG/pyflwor>`_. The Pyflwor
query language is a query language that is inspired by the
`XQuery language <https://www.w3.org/TR/xquery-31/>`_, and is probably the easiest
way to make simple queries. Let's convert the previous example to a Pyflwor query:

.. code-block::

    def run(traSMAPy: TraSMAPy):
        """execute the TraCI control loop"""
        for i in range(100):
            v = traSMAPy.users.createVehicle(f"v{i}")
            v.speed = 10

        while traSMAPy.minExpectedNumber > 0:
            traSMAPy.doSimulationStep()

            print(traSMAPy.query("return sum(<network/edges/CO2Emissions>)"))

        traSMAPy.closeSimulation()


Since we are interested in collecting this statistic for each simulation tick, we can
register the query to be executed every simulation tick. This can be done by using the
`registerQuery` method of the `TraSMAPy` class. Let's register the previous query
(note that you need to provide a name for registered queries):

.. code-block::
    def run(traSMAPy: TraSMAPy):
        """execute the TraCI control loop"""
        for i in range(100):
            v = traSMAPy.users.createVehicle(f"v{i}")
            v.speed = 10

        traSMAPy.registerQuery("Total CO2 Emissions", "return sum(<network/edges/CO2Emissions>)")

        while traSMAPy.minExpectedNumber > 0:
            traSMAPy.doSimulationStep()

            print(traSMAPy.collectedStatistics)

        traSMAPy.closeSimulation()

As you can see, the `collectedStatistics` attribute of the `TraSMAPy` class contains
all the statistics collected by the registered queries, organized by tick and name.
