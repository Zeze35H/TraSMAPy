# TraSMAPy ITS API - Project Specification

## Group members

- Ana Inês Oliveira de Barros -- <up201806593@fe.up.pt>
- João de Jesus Costa -- <up201806560@fe.up.pt>
- João António Cardoso Vieira e Basto de Sousa -- <up201806613@fe.up.pt>

## Project Introduction

Intelligent transportation systems (ITS) has been a domain with progressively
more relevance when tackling problems related to the growing urban traffic
volume in modern cities. Simulations are a valuable tool to explore hypothesis
and make decisions about strategies to tackle these problems: traffic
congestion, lack of parking spots, etc...

Although simulations are valuable, there is a barrier of entry to people without
an informatics background, e.g., traffic-engineers. As such, there is space in
the market for the development of utilities that **abstract** _low-level_
simulation concepts into _higher-level_ real-life concepts.

The objective of this project is to create a ITS-related meta-model, supported
by an API that makes it easier for researchers to instantiate it in multiple
scenarios. This API should streamline the process of creating simulations of
transport systems in [SUMO traffic simulator](https://www.eclipse.org/sumo).

To demonstrate the usage of the API, we will model and simulate a simple
scenario comparing policies to alleviate traffic congestion involving
individual/private vehicles and collective/public transport.

## API concepts

Each API concept belongs to one of three categories: user, infrastructure and
regulator.

### User

#### Vehicles (+ occupation)

- Private vehicles (single or multiple occupants)
- Public transport
- Emergency vehicle

#### Vehicle fuel consumption/CO2 emissions

- Eletric
- Traditional combustion

#### Driver

- Human driver
- (Connected) autonomous vehicle

### Infrastructure

- Road types (low capacity road/highway)
- Intersection/Junction
- Traffic light (simple or with communication mechanisms)
- Parking lots

### Regulator

- Road pricing schemes
- Zones with regulated/restricted access
- Ramp metered junction
- Regulated parking lots (booking / auction / reserved spaces)

#### Metrics

- Throughput at junction
- Traffic congestion
  - Time stopped / Number of vehicles
- Number of vehicles
- Number of passengers (people per car)
- CO2 emissions
- Avg. vehicle tool:
  - Based on road pricing schemes
- Road usage
  - Based on road capacity
- Parking lot lotation
  - Including umber of vehicles without parking available

## Example usage

Which topics to use for the following scenario:

> Comparisons between individual (private vehicle) and collective (public
> transport) policies to alleviate traffic congestion.

1. Predictive and speculative simulation
2. Exogenous variables of the model:
   - Controllable: number vehicles, number of passengers, road lane policy
     (public transportation-exclusive lanes)
   - Uncontrollable: road speed limits, number of lanes
3. Endogenous variables of the model:
   - Passenger throughtput
   - Time stopped
   - Traffic density/congestion
   - Total vehicle emissions
   - Money spent on road pricing scheme
   - Average vehicle speed
4. Performance metrics:
   - Passenger throughtput
   - Time stopped
   - Average time to reach destination (for private and public transport)
   - Money spent on road pricing scheme
   - Total vehicle emissions
5. Key performance indicators (KPI):
   - Traffic density/congestion
   - Cost per passenger (related to road pricing scheme)
   - Difference between the private and public transportation time taken to
     reach destination
   - Emission in relation to cost for each passenger
   - Time(%) under the road lower speed limit (due to traffic congestion)
6. Operational policies:
   - Road lane with exclusive access for public transport
   - Road lanes with extra costs for private vehicles
   - Penalise private vehicles that transport few passengers/aren't full
7. Possible data collection methods, techniques and tools:
   - No data collection
   - Possibly collect map information for OSM (Open Street Map)
8. Models validation:
   - Not possible without access to real world past data.
9. Possible scenarios to be simulated:
   - Simple road with 2 lanes in each direction (only private transportation)
   - Similar scenarios but considering public transportation (25%, 50%, 75%, and
     100% of the passengers)
   - Repeat previous scenarios but with additional roads and intersections
   - Highway-like scenario where there is an "external" influx and efflux of
     vehicles
   - Limiting the use of the right-most lane exclusively to public
     transportation
10. What operational decisions could be supported by the simulation models?
    - Find new road policies/pricing schemes to reduce traffic congestion and
      emissions
    - The increase or decrease in the number of lanes of certain roads

### API Concepts

- User:
  - Private vehicle
  - Public transport
- Regulator:
  - Road pricing schemes
  - Zones with regulated/restricted access
  - Metrics:
    - Throughput at junction
    - Traffic congestion
    - Number of passenger

## Coding

The API will be based on the structure and ideas of the
[TraSMAPI framework](https://doi.org/10.1007/s13748-012-0013-y) and implemented
in python to lower the barrier of entry. We're only targeting
[SUMO traffic simulator](https://www.eclipse.org/sumo), so the API will interact
with it through the
[TraCI API](https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html).

### Tools

- [Python](https://www.python.org)
- [SUMO (Simulation of Urban MObility)](https://www.eclipse.org/sumo)
- [TraCI](https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html)
