## Lista 5: N-Body Gravitational Simulation

Simulates gravitational interactions between N bodies using numerical integration. Demonstrates orbital mechanics, chaos theory, and energy conservation.

## What Was Improved

- ❌ **Original**: Only Euler integration (poor energy conservation)
- ✅ **Improved**: Multiple integrators (Euler, RK4, Verlet) with accuracy tradeoffs
- ❌ **Original**: No energy tracking
- ✅ **Improved**: Energy conservation analysis
- ❌ **Original**: Hardcoded parameters
- ✅ **Improved**: Configuration-based setup with CLI
- ❌ **Original**: Mixed simulation and I/O
- ✅ **Improved**: Modular design with Strategy pattern for integrators

## Usage

```bash
# Binary orbit with RK4 integrator
python src/lista5_nbody/nbody_simulation.py --integrator rk4 --dt 0.01 --t-max 10

# Compare integrators
python src/lista5_nbody/nbody_simulation.py --integrator euler --verbose
python src/lista5_nbody/nbody_simulation.py --integrator verlet --verbose
```

## Key Concepts

- **Two-body problem**: Analytically solvable (Kepler orbits)
- **Three-body problem**: Chaotic (discovered by Poincaré)
- **Symplectic integrators**: Preserve energy (Verlet)
- **Energy conservation**: Test of numerical accuracy

Output: `output/lista5_nbody/data/trajectories.txt`
