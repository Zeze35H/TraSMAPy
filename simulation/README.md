# Simulation of UVAR Policies in Urban Environments

With a steady increase in population density in urban centres, it has become essential to guarantee inhabitants’ well-being and
quality of life. Urban Vehicle Access Regulations (UVAR) include policies to reduce vehicle use in urban environments.

This project provides the implementation of two urban restriction policies on SUMO platform with the help of TraSMAPy. 
These are used in a simulation of a fake citie's centre road network.


## Usage
### Simulation
To run the simulation:
```
usage: run.py [-h] [--sumocfg SUMOCFG] [-n NO_VEHICLES] [--steps STEPS] [--forbid] [--tolls] [--stats-path STATS_PATH]

options:
  -h, --help            show this help message and exit
  --sumocfg SUMOCFG     path to sumocfg
  -n NO_VEHICLES, --no-vehicles NO_VEHICLES
                        number of vehicles to create
  --steps STEPS         maximum simulation steps
  --forbid              run the forbid scenario (restrict access)
  --tolls               run the tolls scenario (toll fees)
  --stats-path STATS_PATH
                        path to the output statistics file
```

### Statistics
To generate charts from the collected statistics:

``` 
python generate_charts.py --stats-files [scenario_name],[path_to_stats_file]
```

Example for generating charts from three simulations:
```
 python generate_charts.py --stats-files Baseline,./stats/baseline.csv Tolls,./stats/tolls.csv Forbid,./stats/forbid.csv
```

> **Note:** a set of scripts for generating charts with SUMO's visualization scripts is available in [scripts](./scripts/) 

## Authors
- Ivo Saavedra - ivosaavedra@gmail.com
- Telmo Baptista - up201806554@edu.fe.up.pt
- Ricardo Fontão - up201806317@edu.fe.up.pt

## LICENSE
This project has an open source [MIT License](./LICENSE) 

