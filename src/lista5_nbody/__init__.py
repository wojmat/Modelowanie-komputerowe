"""Lista 5: N-Body Gravitational Simulation

Simulates gravitational interactions between multiple bodies using numerical integration.
Includes energy conservation analysis, orbital stability, and chaos theory demonstrations.

Physics concept: Classical mechanics, gravitational dynamics, chaos theory
"""

from .nbody_simulation import NBodySimulation, Body, NBodyConfig
from .integrators import EulerIntegrator, RK4Integrator, VerletIntegrator

__all__ = [
    'NBodySimulation',
    'Body',
    'NBodyConfig',
    'EulerIntegrator',
    'RK4Integrator',
    'VerletIntegrator',
]
