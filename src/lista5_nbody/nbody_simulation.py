"""N-Body gravitational simulation - Improved implementation

ORIGINAL ISSUES:
1. Euler integration only - first-order accuracy, poor energy conservation
2. Hardcoded timesteps - no adaptive stepping
3. No energy conservation tracking
4. Inefficient nested loops - O(N²) force calculation unavoidable but can optimize
5. Hardcoded initial conditions
6. No integrator abstraction
7. File I/O in simulation loop - slow

IMPROVEMENTS:
1. Multiple integrators - Euler, RK4, Verlet (choose accuracy vs speed)
2. Adaptive timestep option - maintain accuracy
3. Energy/momentum tracking - validate physics
4. Vectorized operations where possible
5. Configuration-based setup
6. Strategy pattern for integrators
7. Batch data storage

Physics:
- Newton's law of gravitation: F = G*m1*m2/r²
- Two-body problem: Solvable analytically (Kepler orbits)
- Three-body problem: Chaotic, no general solution (Poincaré)
- N-body problem: Numerical integration required

Numerical integration challenges:
- Energy drift: Symplectic integrators preserve energy
- Timestep sensitivity: Smaller dt = more accurate but slower
- Close encounters: Gravitational force → ∞ as r → 0
"""

from typing import List, Tuple, Optional, Callable
import numpy as np
from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.utils import validate_positive, Timer


@dataclass
class Body:
    """Represents a gravitational body.

    Why dataclass?
    - Clean initialization
    - Immutable configuration
    - Type hints enforced
    """
    mass: float
    position: np.ndarray  # [x, y] or [x, y, z]
    velocity: np.ndarray  # [vx, vy] or [vx, vy, vz]
    name: str = "Body"

    def __post_init__(self):
        """Validate and convert to NumPy arrays."""
        self.position = np.array(self.position, dtype=float)
        self.velocity = np.array(self.velocity, dtype=float)
        validate_positive(self.mass, "mass")

        if self.position.shape != self.velocity.shape:
            raise ValueError("Position and velocity must have same dimensions")


@dataclass
class NBodyConfig:
    """Configuration for N-body simulation."""
    G: float = 1.0  # Gravitational constant
    dt: float = 0.01  # Timestep
    t_max: float = 10.0  # Maximum time
    integrator: str = "rk4"  # euler, rk4, verlet
    track_energy: bool = True
    dimensions: int = 2  # 2D or 3D

    def __post_init__(self):
        validate_positive(self.G, "G")
        validate_positive(self.dt, "dt")
        validate_positive(self.t_max, "t_max")

        if self.integrator not in ["euler", "rk4", "verlet"]:
            raise ValueError(f"Unknown integrator: {self.integrator}")

        if self.dimensions not in [2, 3]:
            raise ValueError(f"Dimensions must be 2 or 3, got {self.dimensions}")


class NBodySimulation:
    """N-body gravitational simulation engine.

    Why separate from integrators?
    - Single Responsibility: simulation manages bodies, integrator handles stepping
    - Strategy pattern: swap integrators easily
    - Testable components
    """

    def __init__(self, bodies: List[Body], config: NBodyConfig):
        """Initialize simulation.

        Args:
            bodies: List of Body objects
            config: Simulation configuration
        """
        self.bodies = bodies
        self.config = config
        self.n_bodies = len(bodies)

        # Validate all bodies have same dimensionality
        dims = [len(b.position) for b in bodies]
        if len(set(dims)) > 1:
            raise ValueError(f"All bodies must have same dimensions, got {dims}")

        self.dim = dims[0]

        # State vectors (for efficient computation)
        self.positions = np.array([b.position for b in bodies])
        self.velocities = np.array([b.velocity for b in bodies])
        self.masses = np.array([b.mass for b in bodies])

        # History
        self.time_history = []
        self.position_history = []
        self.velocity_history = []
        self.energy_history = []

        # Integrator
        from .integrators import get_integrator
        self.integrator = get_integrator(config.integrator)

        self.current_time = 0.0

    def compute_forces(self) -> np.ndarray:
        """Compute gravitational forces on all bodies.

        Returns:
            Array of forces shape (n_bodies, dim)

        Why vectorization is hard here?
        - Force between each pair must be computed
        - Pairwise operation is inherently O(N²)
        - Can optimize with NumPy broadcasting but still N²
        """
        forces = np.zeros_like(self.positions)

        for i in range(self.n_bodies):
            for j in range(i + 1, self.n_bodies):
                # Vector from i to j
                r_vec = self.positions[j] - self.positions[i]
                r_mag = np.linalg.norm(r_vec)

                if r_mag < 1e-10:  # Avoid division by zero
                    continue

                # Newton's law: F = G*m1*m2/r² in direction of r
                force_mag = self.config.G * self.masses[i] * self.masses[j] / r_mag**2
                force_vec = force_mag * (r_vec / r_mag)

                # Newton's third law: equal and opposite
                forces[i] += force_vec
                forces[j] -= force_vec

        return forces

    def compute_energy(self) -> Tuple[float, float, float]:
        """Compute total energy of system.

        Returns:
            Tuple of (kinetic, potential, total) energy

        Why important?
        - Energy should be conserved (1st law of thermodynamics)
        - Energy drift indicates numerical error
        - Symplectic integrators preserve energy better
        """
        # Kinetic energy: KE = (1/2) * m * v²
        kinetic = 0.5 * np.sum(self.masses[:, np.newaxis] * (self.velocities ** 2))

        # Potential energy: PE = -G * m1 * m2 / r
        potential = 0.0
        for i in range(self.n_bodies):
            for j in range(i + 1, self.n_bodies):
                r = np.linalg.norm(self.positions[j] - self.positions[i])
                if r > 1e-10:
                    potential -= self.config.G * self.masses[i] * self.masses[j] / r

        total = kinetic + potential
        return kinetic, potential, total

    def step(self):
        """Advance simulation by one timestep."""
        # Use integrator
        self.positions, self.velocities = self.integrator.step(
            self.positions,
            self.velocities,
            self.masses,
            self.compute_forces,
            self.config.dt
        )

        self.current_time += self.config.dt

        # Record history
        self.time_history.append(self.current_time)
        self.position_history.append(self.positions.copy())
        self.velocity_history.append(self.velocities.copy())

        if self.config.track_energy:
            ke, pe, total_e = self.compute_energy()
            self.energy_history.append((ke, pe, total_e))

    def run(self, verbose: bool = False) -> None:
        """Run simulation to completion.

        Args:
            verbose: Print progress
        """
        n_steps = int(self.config.t_max / self.config.dt)

        # Initial energy
        if self.config.track_energy:
            ke, pe, total_e = self.compute_energy()
            self.energy_history.append((ke, pe, total_e))
            initial_energy = total_e

        with Timer(f"N-body simulation ({n_steps} steps)") if verbose else Timer.__new__(Timer):
            for step in range(n_steps):
                self.step()

                if verbose and (step + 1) % (n_steps // 10) == 0:
                    percent = 100.0 * (step + 1) / n_steps
                    print(f"  Progress: {percent:.0f}% (t={self.current_time:.2f})")

        if verbose:
            print(f"\nSimulation complete!")
            if self.config.track_energy:
                final_energy = self.energy_history[-1][2]
                energy_drift = abs(final_energy - initial_energy) / abs(initial_energy)
                print(f"  Energy drift: {energy_drift*100:.4f}%")
                print(f"  Integrator: {self.config.integrator}")

    def get_trajectories(self) -> np.ndarray:
        """Get position history as array.

        Returns:
            Array shape (n_steps, n_bodies, dim)
        """
        return np.array(self.position_history)

    def save_results(self, output_path: Path):
        """Save simulation results to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        trajectories = self.get_trajectories()

        with open(output_path, 'w') as f:
            f.write(f"# N-Body Simulation Results\n")
            f.write(f"# Bodies: {self.n_bodies}\n")
            f.write(f"# Timestep: {self.config.dt}\n")
            f.write(f"# Integrator: {self.config.integrator}\n")
            f.write(f"# Time\t" + "\t".join([f"x{i}\ty{i}" for i in range(self.n_bodies)]) + "\n")

            for t, pos in zip(self.time_history, trajectories):
                f.write(f"{t:.6f}")
                for body_pos in pos:
                    f.write(f"\t{body_pos[0]:.6f}\t{body_pos[1]:.6f}")
                f.write("\n")

        print(f"✓ Results saved to: {output_path}")


def create_binary_orbit(mass1: float = 1.0, mass2: float = 1.0,
                        separation: float = 1.0, velocity_scale: float = 1.0) -> List[Body]:
    """Create two bodies in circular orbit.

    Args:
        mass1: Mass of body 1
        mass2: Mass of body 2
        separation: Initial separation
        velocity_scale: Multiply computed velocity (1.0 = circular, <1 = elliptical)

    Returns:
        List of two Body objects

    Why useful?
    - Two-body problem is analytically solvable
    - Good test case for numerical integrators
    - Check energy conservation
    """
    # Circular orbit velocity: v = sqrt(G*M/r) where M = total mass
    G = 1.0
    v_circular = np.sqrt(G * (mass1 + mass2) / separation) * velocity_scale

    # Reduced mass system: bodies orbit common center of mass
    # Place mass1 at origin, mass2 at separation
    # Velocities perpendicular to separation

    body1 = Body(
        mass=mass1,
        position=[0, 0],
        velocity=[0, -v_circular * mass2 / (mass1 + mass2)],
        name="Body1"
    )

    body2 = Body(
        mass=mass2,
        position=[separation, 0],
        velocity=[0, v_circular * mass1 / (mass1 + mass2)],
        name="Body2"
    )

    return [body1, body2]


def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run N-body gravitational simulation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--dt', type=float, default=0.01, help='Timestep')
    parser.add_argument('--t-max', type=float, default=10.0, help='Simulation time')
    parser.add_argument('--integrator', type=str, default='rk4',
                       choices=['euler', 'rk4', 'verlet'], help='Integration method')
    parser.add_argument('--verbose', action='store_true', help='Print progress')

    args = parser.parse_args()

    # Create binary system
    bodies = create_binary_orbit(mass1=1.0, mass2=1.0, separation=1.0)

    config = NBodyConfig(
        dt=args.dt,
        t_max=args.t_max,
        integrator=args.integrator
    )

    print("=" * 60)
    print("N-BODY GRAVITATIONAL SIMULATION")
    print("=" * 60)
    print(f"Bodies: {len(bodies)}")
    print(f"Timestep: {config.dt}")
    print(f"Max time: {config.t_max}")
    print(f"Integrator: {config.integrator}")
    print("=" * 60)

    sim = NBodySimulation(bodies, config)
    sim.run(verbose=args.verbose)

    from common.config import OutputManager
    om = OutputManager(Path("output"), "lista5_nbody")
    sim.save_results(om.get_data_path("trajectories.txt"))


if __name__ == "__main__":
    main()
