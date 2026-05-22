# OSI-Gen

Generate `OpenSimulationInterface` (`OSI`) trace files carrying `GroundTruth` information compliant with 
the [OmegaPrime](https://github.com/ika-rwth-aachen/omega-prime/blob/main/docs/omega_prime_specification.md) format developed in the Synergies project. For more details about the requirements, check [`requirements.md`](requirements.md).

> [!NOTE]
> This open source project is maintained by [RISE Research Institutes of Sweden](https://ri.se/). See license file for open source license information.

## Features

 - **Carla trajectory recording** (Python ≥ 3.8): Record trajectories of vehicles inside a Carla simulation with the help of a simple function call inside of a `Carla` client that is `tick()`-ing the simulation
 - **Recording conversion** (Python ≥ 3.10): Convert stored trajectory recordings into [OmegaPrime](https://github.com/ika-rwth-aachen/omega-prime)-compliant OSI trace files, either programmatically via `Traj2OSI` or from the command line

## Installation

| Use case | Python | Install command |
|----------|--------|-----------------|
| Store trajectories from Carla | ≥ 3.8 | `pip install .` |
| Convert stored trajectories to OmegaPrime / OSI | ≥ 3.10 | `pip install .[cli]` |

### Recording only (Python ≥ 3.8)

```bash
pip install .
```

This installs the core library with `polars` and `carla`. You can record trajectories inside a Carla simulation and save them as parquet files.

### CLI / conversion mode (Python ≥ 3.10)

```bash
pip install .[cli]
```

This additionally installs `betterosi`, `rich-argparse`, and `omega-prime`, enabling the `python -m traj_convert` CLI and programmatic OSI conversion via `Traj2OSI`.

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

This saves the trajectory recording to a `parquet` file with a timestamped filename.

### Convert Recording

The trajectories are converted to OSI format from the command line (requires `.[cli]` install):

```bash
python -m traj_convert traj.parquet 752 0.1.0 "" "Town01.xodr" -o output.osi
```

To create an [OmegaPrime](https://github.com/ika-rwth-aachen/omega-prime)-compliant MCAP file with an embedded OpenDRIVE map, use the `--omega-prime` flag:

```bash
python -m traj_convert traj.parquet 752 0.1.0 "+proj=..." "Town01.xodr" --omega-prime -o output.mcap
```

Run `python -m traj_convert --help` for details on all arguments.

## Visualization

See [`jupyter/omega_prime_viz.ipynb`](jupyter/omega_prime_viz.ipynb). Activate the development environment before accessing the notebook.

## Development

To further develop the code, use the `conda` environment file in `environment.yml`:
```bash
conda env create -f environment.yml
```

## Acknowledgments

The generation of OSI files in this project relies on the [`betterosi`](https://github.com/ika-rwth-aachen/betterosi) package.

This software was developed as part of the [Synergies](https://synergies-ccam.eu/) project.

![Synergies-logo](media/synergies.png)

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or European Climate, Infrastructure and Environment Executive Agency (CINEA). Neither the European Union nor the granting authority can be held responsible for them.
