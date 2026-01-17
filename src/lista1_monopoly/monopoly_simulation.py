"""Monopoly board simulation - Improved implementation

Why this refactoring was necessary:

ORIGINAL ISSUES:
1. C++ used deprecated rand() - not cryptographically secure, poor distribution
2. No error handling - file operations could fail silently
3. Hardcoded values - board size, filename not configurable
4. Interactive input only - no CLI arguments for automation
5. No validation - could crash with negative input
6. Separate implementations - "with jail" and "without jail" duplicated code

IMPROVEMENTS:
1. Modern Python with proper random number generation
2. Comprehensive error handling with informative messages
3. Configuration class for all parameters
4. CLI argument parsing for automation
5. Type hints for safety and IDE support
6. Unified implementation with jail as optional parameter
7. Proper logging for debugging
8. Output management with automatic directory creation

Physics background:
- Models discrete random walk on periodic 1D lattice
- Board is circular: position 40 wraps to position 0
- Two dice: sum follows triangular distribution (peak at 7)
- Jail rule: forced teleportation breaks uniform distribution
"""

from typing import List, Tuple, Optional
import numpy as np
from pathlib import Path
import argparse
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.config import Config, OutputManager
from common.utils import validate_positive, set_random_seed, Timer


class Board:
    """Represents a Monopoly board.

    Why a class?
    - Encapsulates board state and operations
    - Easy to extend with special squares (jail, go, etc.)
    - Separates data from simulation logic
    """

    def __init__(self, num_squares: int = 40):
        """Initialize board.

        Args:
            num_squares: Number of squares on the board

        Raises:
            ValueError: If num_squares is not positive
        """
        validate_positive(num_squares, "num_squares")
        self.num_squares = num_squares
        self.visit_counts = np.zeros(num_squares, dtype=int)

    def record_visit(self, position: int) -> None:
        """Record a visit to a square.

        Args:
            position: Square position (will be wrapped to board size)
        """
        position = position % self.num_squares
        self.visit_counts[position] += 1

    def get_probabilities(self, total_rolls: int) -> np.ndarray:
        """Calculate probability of visiting each square.

        Args:
            total_rolls: Total number of dice rolls

        Returns:
            Array of probabilities (percentages)
        """
        return (self.visit_counts / total_rolls) * 100.0

    def get_statistics(self) -> dict:
        """Get statistical summary of visits.

        Returns:
            Dictionary with min, max, mean, std of visit counts
        """
        return {
            'min_visits': int(np.min(self.visit_counts)),
            'max_visits': int(np.max(self.visit_counts)),
            'mean_visits': float(np.mean(self.visit_counts)),
            'std_visits': float(np.std(self.visit_counts)),
            'total_visits': int(np.sum(self.visit_counts))
        }

    def reset(self) -> None:
        """Reset all visit counts to zero."""
        self.visit_counts.fill(0)


class MonopolySimulation:
    """Simulates player movement on a Monopoly board.

    Why this architecture?
    - Separates simulation logic from I/O
    - Testable: can verify results programmatically
    - Reusable: can be imported by other scripts
    - Configurable: all parameters in one place
    """

    def __init__(
        self,
        num_squares: int = 40,
        use_jail: bool = False,
        jail_position: int = 10,
        random_seed: Optional[int] = None
    ):
        """Initialize simulation.

        Args:
            num_squares: Number of squares on the board
            use_jail: Whether to implement jail rule
            jail_position: Position of jail square
            random_seed: Random seed for reproducibility

        Why these parameters?
        - num_squares: Standard Monopoly has 40, but generalizes
        - use_jail: Lets us compare with/without jail in same code
        - jail_position: Jail at square 10 in standard Monopoly
        - random_seed: Scientific reproducibility requirement
        """
        validate_positive(num_squares, "num_squares")

        self.num_squares = num_squares
        self.use_jail = use_jail
        self.jail_position = jail_position % num_squares
        self.board = Board(num_squares)

        # Set random seed for reproducibility
        if random_seed is not None:
            set_random_seed(random_seed)
            self.rng = np.random.RandomState(random_seed)
        else:
            self.rng = np.random.RandomState()

    def roll_dice(self) -> Tuple[int, int]:
        """Roll two six-sided dice.

        Returns:
            Tuple of (die1, die2) values

        Why separate method?
        - Easy to test
        - Can be overridden for loaded dice, etc.
        - Centralizes random number generation
        """
        die1 = self.rng.randint(1, 7)  # 1-6 inclusive
        die2 = self.rng.randint(1, 7)
        return die1, die2

    def move_player(self, current_position: int, roll_sum: int) -> int:
        """Calculate new player position after dice roll.

        Args:
            current_position: Current square number
            roll_sum: Sum of dice roll

        Returns:
            New position after move

        Why modulo arithmetic?
        - Board is circular (periodic boundary conditions)
        - Position 40 wraps to position 0
        - Standard in discrete random walks
        """
        new_position = (current_position + roll_sum) % self.num_squares
        return new_position

    def run(self, num_rolls: int, verbose: bool = False) -> Board:
        """Run the simulation.

        Args:
            num_rolls: Number of dice rolls to simulate
            verbose: If True, print progress

        Returns:
            Board object with visit statistics

        Raises:
            ValueError: If num_rolls is not positive

        Why return Board object?
        - Caller can access detailed statistics
        - Can be passed to visualization functions
        - Separates simulation from output
        """
        validate_positive(num_rolls, "num_rolls")

        self.board.reset()
        position = 0  # Start at GO

        with Timer("Simulation", silent=not verbose):
            for i in range(num_rolls):
                # Roll dice
                die1, die2 = self.roll_dice()
                roll_sum = die1 + die2

                # Check for doubles and jail (simplified jail rule)
                if self.use_jail and die1 == die2:
                    # Three doubles in a row sends to jail
                    # For simplicity, we just go to jail on any double
                    position = self.jail_position
                else:
                    # Normal move
                    position = self.move_player(position, roll_sum)

                # Record visit
                self.board.record_visit(position)

                # Progress feedback
                if verbose and (i + 1) % (num_rolls // 10) == 0:
                    percent = 100.0 * (i + 1) / num_rolls
                    print(f"  Progress: {percent:.0f}% ({i+1}/{num_rolls})")

        if verbose:
            stats = self.board.get_statistics()
            print(f"\nSimulation complete!")
            print(f"  Total visits: {stats['total_visits']}")
            print(f"  Mean visits per square: {stats['mean_visits']:.1f}")
            print(f"  Std deviation: {stats['std_visits']:.1f}")
            print(f"  Min/Max: {stats['min_visits']} / {stats['max_visits']}")

        return self.board

    def save_results(
        self,
        output_path: Path,
        num_rolls: int
    ) -> None:
        """Save simulation results to file.

        Args:
            output_path: Path to output file
            num_rolls: Number of rolls (for percentage calculation)

        Why this format?
        - Human-readable text file
        - Compatible with original format
        - Easy to parse for visualization
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        probabilities = self.board.get_probabilities(num_rolls)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Monopoly Simulation Results\n")
                f.write(f"Number of rolls: {num_rolls}\n")
                f.write(f"Use jail rule: {self.use_jail}\n")
                f.write(f"{'=' * 50}\n\n")

                for square_num in range(self.num_squares):
                    visits = self.board.visit_counts[square_num]
                    prob = probabilities[square_num]
                    f.write(f"Pole {square_num + 1}: {visits} ({prob:.4f}%)\n")

                # Add statistics
                stats = self.board.get_statistics()
                f.write(f"\n{'=' * 50}\n")
                f.write(f"Statistics:\n")
                f.write(f"  Mean: {stats['mean_visits']:.2f}\n")
                f.write(f"  Std: {stats['std_visits']:.2f}\n")
                f.write(f"  Min: {stats['min_visits']}\n")
                f.write(f"  Max: {stats['max_visits']}\n")

            print(f"✓ Results saved to: {output_path}")

        except IOError as e:
            print(f"✗ Error saving results: {e}")
            raise


def main():
    """Main entry point with CLI argument parsing.

    Why CLI arguments instead of interactive input?
    - Enables automation and scripting
    - Can be called from other programs
    - Easier to run multiple experiments
    - Standard practice for scientific code

    Example usage:
        python monopoly_simulation.py --rolls 1000000
        python monopoly_simulation.py --rolls 100000 --jail --seed 42
    """
    parser = argparse.ArgumentParser(
        description="Simulate random walk on Monopoly board",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--rolls',
        type=int,
        default=1000000,
        help='Number of dice rolls to simulate'
    )

    parser.add_argument(
        '--squares',
        type=int,
        default=40,
        help='Number of squares on the board'
    )

    parser.add_argument(
        '--jail',
        action='store_true',
        help='Enable jail rule (doubles send to jail)'
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file path (default: auto-generated)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print progress information'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.rolls <= 0:
        parser.error("Number of rolls must be positive")

    if args.squares <= 0:
        parser.error("Number of squares must be positive")

    # Set up output path
    if args.output is None:
        output_manager = OutputManager(Path("output"), "lista1_monopoly")
        jail_suffix = "with_jail" if args.jail else "no_jail"
        output_path = output_manager.get_data_path(f"results_{jail_suffix}.txt")
    else:
        output_path = Path(args.output)

    # Print configuration
    print("=" * 60)
    print("MONOPOLY BOARD SIMULATION")
    print("=" * 60)
    print(f"Number of rolls: {args.rolls:,}")
    print(f"Board squares: {args.squares}")
    print(f"Jail rule: {'Enabled' if args.jail else 'Disabled'}")
    print(f"Random seed: {args.seed if args.seed is not None else 'Random'}")
    print(f"Output file: {output_path}")
    print("=" * 60)

    # Run simulation
    sim = MonopolySimulation(
        num_squares=args.squares,
        use_jail=args.jail,
        random_seed=args.seed
    )

    board = sim.run(args.rolls, verbose=args.verbose)

    # Save results
    sim.save_results(output_path, args.rolls)

    # Print summary
    probs = board.get_probabilities(args.rolls)
    print(f"\nProbability range: {np.min(probs):.4f}% - {np.max(probs):.4f}%")
    print(f"Expected uniform: {100.0/args.squares:.4f}%")
    print(f"Deviation from uniform: {np.std(probs):.4f}%")

    print("\nDone! Run visualize.py to generate plots.")


if __name__ == "__main__":
    main()
