# OSI-Gen

Create a python functionality that enables to generate `OpenSimulationInterface` (`OSI`) trace files carrying `GroundTruth` information compliant with 
the [OmegaPrime](https://github.com/ika-rwth-aachen/omega-prime/blob/main/docs/omega_prime_specification.md) format developed in the Synergies project. For more details about the requirements, check [`requirements.md`](requirements.md).

## Features

 - **Carla trajectory recording**: Record trajectories of vehicles inside a Carla simulation with the help of a simple function call inside of a `Carla` client that is `tick()`-ing the simulation
 - **Recording conversion**: Convert recordings into an `OmegaPrime` / OSI trace file from the command line

## Quickstart

Checkout the *Quickstart* section inside [python/README.md](python/README.md).

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