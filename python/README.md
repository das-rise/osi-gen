# Trajectory Converter

Create a python functionality that enables to generate `OpenSimulationInterface` (`OSI`) trace files carrying `GroundTruth` information compliant with 
the [OmegaPrime](https://github.com/ika-rwth-aachen/omega-prime/blob/main/docs/omega_prime_specification.md) format developed in the Synergies project. For more details about the requirements, check [`requirements.md`](../requirements.md).

## Features

 - **Carla trajectory recording**: Record trajectories of vehicles inside a Carla simulation with the help of a simple function call inside of a `Carla` client that is `tick()`-ing the simulation
 - **Recording conversion**: Convert recordings into an `OmegaPrime` / OSI trace file from the command line
 - **Extendability**: From the internal recordings format (easily-readable Polars dataframe), convert to additional output formats such as ASAM OpenLabel

## Quickstart

Install with `pip` from inside this folder:

```bash
pip install .
```

### Generate Recording

First, the trajectories inside a `Carla` simulation are recorded. To do this, a `polars` DataFrame containing annotations for every frame of a `Carla` simulation is generated.
Inside a `carla.Client`, this can be done as such:

```python

from traj_convert import carla2traj
...

traj_recorder = carla2traj.Carla2Traj(world, debug = False) # setup a Trajectory recorder

while True:
    world.tick()
    snapshot = world.get_snapshot()
    traj_recorder.process_world_snapshot(snapshot)
    ...

traj_recorder.save()
```

This saves the trajecory recording to a `parquet` file with a timestamped filename.

### Convert Recording

Next, the trajectories are converted. For this, `carla2traj.py` is run on the parquet file directly from the command line. The `help` section explains how the conversion can be done:

```bash
user:~$ python -m traj_convert --help
```

## Acknowledgments

The generation of OSI files in this project relies on the [`betterosi`](https://github.com/ika-rwth-aachen/betterosi) package.

This software was developed as part of the [Synergies](https://synergies-ccam.eu/) project.

![Synergies-logo](../media/synergies.png)

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or European Climate, Infrastructure and Environment Executive Agency (CINEA). Neither the European Union nor the granting authority can be held responsible for them.