# OSI-Gen

This work is performed as part of the [Synergies](https://synergies-ccam.eu/) project.

## Goal

Create a python functionality that enables to generate `OpenSimulationInterface` (`OSI`) trace files carrying `GroundTruth` information compliant with 
the [OmegaPrime](https://github.com/ika-rwth-aachen/omega-prime/blob/main/docs/omega_prime_specification.md) format developed in the Synergies project.

## How-to

First, a `polars` DataFrame containing annotations for every frame of a `Carla` simulation is generated.
Inside a `carla.Client`, this can be done as such:

```python

traj_recorder = carla2traj.Carla2Traj(world, debug = False) # setup a Trajectory recorder

while True:
    world.tick()
    snapshot = world.get_snapshot()
    traj_recorder.process_world_snapshot(snapshot)
    ...

traj_recorder.save()
```

This saves the trajecory recording to a `parquet` file.
