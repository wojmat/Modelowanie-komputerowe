"""Visualization for Monopoly simulation results

Why this refactoring was necessary:

ORIGINAL ISSUES:
1. Hardcoded data - manually copied from output file
2. Hardcoded absolute path - C:/Users/Administrator/Desktop/...
3. No file reading - data not loaded from simulation output
4. Duplicated matplotlib code - same setup as other projects
5. No error handling - would crash if file missing

IMPROVEMENTS:
1. Automatic file reading from simulation output
2. Portable paths using OutputManager
3. Reusable Plotter class from common library
4. Error handling with informative messages
5. CLI arguments for flexibility
6. Can compare multiple simulations
"""

from typing import List, Tuple
import numpy as np
from pathlib import Path
import argparse
import sys
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.plotting import Plotter, save_plot
from common.config import OutputManager


def parse_results_file(filepath: Path) -> Tuple[List[int], List[float]]:
    """Parse simulation results from output file.

    Args:
        filepath: Path to results file

    Returns:
        Tuple of (square_numbers, probabilities)

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid

    Why this function?
    - Original code had hardcoded data
    - Now we read directly from simulation output
    - Eliminates manual data copying errors
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Results file not found: {filepath}")

    square_numbers = []
    probabilities = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Parse lines like: "Pole 1: 24891 (2.4891%)"
                match = re.match(r'Pole (\d+): \d+ \(([\d.]+)%\)', line)
                if match:
                    square_num = int(match.group(1))
                    prob = float(match.group(2))
                    square_numbers.append(square_num)
                    probabilities.append(prob)

    except IOError as e:
        raise IOError(f"Error reading file {filepath}: {e}")

    if not square_numbers:
        raise ValueError(f"No valid data found in {filepath}")

    return square_numbers, probabilities


def visualize_results(
    filepath: Path,
    output_path: Optional[Path] = None,
    title: Optional[str] = None
) -> None:
    """Create visualization of simulation results.

    Args:
        filepath: Path to simulation results file
        output_path: Path to save plot (if None, display only)
        title: Custom plot title

    Why separate visualization?
    - Simulation and plotting are independent concerns
    - Can re-plot without re-running simulation
    - Easy to try different visualization styles
    """
    # Read data
    print(f"Reading results from: {filepath}")
    squares, probabilities = parse_results_file(filepath)

    # Create plot
    import matplotlib.pyplot as plt

    plt.figure(figsize=(14, 7))
    plt.bar(squares, probabilities, color='orange', edgecolor='black', alpha=0.7)

    # Calculate expected uniform probability
    num_squares = len(squares)
    uniform_prob = 100.0 / num_squares

    # Add horizontal line for uniform distribution
    plt.axhline(
        y=uniform_prob,
        color='red',
        linestyle='--',
        linewidth=2,
        label=f'Uniform ({uniform_prob:.3f}%)'
    )

    # Labels and title
    if title is None:
        title = f'Monopoly Board Probability Distribution ({num_squares} squares)'
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Square Number', fontsize=12)
    plt.ylabel('Probability (%)', fontsize=12)

    # Grid and legend
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.legend(fontsize=10)

    # Set y-axis to start from 0
    plt.ylim(0, max(probabilities) * 1.1)

    # Tight layout
    plt.tight_layout()

    # Save or show
    if output_path:
        save_plot(output_path)
    else:
        plt.show()

    plt.close()

    # Print statistics
    print(f"\nStatistics:")
    print(f"  Number of squares: {num_squares}")
    print(f"  Min probability: {min(probabilities):.4f}%")
    print(f"  Max probability: {max(probabilities):.4f}%")
    print(f"  Mean probability: {np.mean(probabilities):.4f}%")
    print(f"  Std deviation: {np.std(probabilities):.4f}%")
    print(f"  Expected uniform: {uniform_prob:.4f}%")


def compare_simulations(
    filepaths: List[Path],
    labels: List[str],
    output_path: Optional[Path] = None
) -> None:
    """Compare multiple simulation results on one plot.

    Args:
        filepaths: List of result file paths
        labels: Labels for each simulation
        output_path: Path to save comparison plot

    Why this function?
    - Easy comparison of jail vs no-jail
    - Visual difference between parameter settings
    - Standard scientific visualization practice
    """
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(len(filepaths), 1, figsize=(14, 5 * len(filepaths)))

    if len(filepaths) == 1:
        axes = [axes]

    for idx, (filepath, label) in enumerate(zip(filepaths, labels)):
        try:
            squares, probabilities = parse_results_file(filepath)

            ax = axes[idx]
            ax.bar(squares, probabilities, color='orange', edgecolor='black', alpha=0.7)

            # Uniform line
            uniform_prob = 100.0 / len(squares)
            ax.axhline(
                y=uniform_prob,
                color='red',
                linestyle='--',
                linewidth=2,
                label=f'Uniform ({uniform_prob:.3f}%)'
            )

            ax.set_title(label, fontsize=12, fontweight='bold')
            ax.set_xlabel('Square Number')
            ax.set_ylabel('Probability (%)')
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            ax.legend()
            ax.set_ylim(0, max(probabilities) * 1.1)

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    plt.tight_layout()

    if output_path:
        save_plot(output_path)
    else:
        plt.show()

    plt.close()


def main():
    """Main entry point with CLI arguments.

    Example usage:
        python visualize.py
        python visualize.py --input results_no_jail.txt
        python visualize.py --compare results_no_jail.txt results_with_jail.txt
    """
    parser = argparse.ArgumentParser(
        description="Visualize Monopoly simulation results",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--input',
        type=str,
        default=None,
        help='Path to simulation results file'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Path to save plot image'
    )

    parser.add_argument(
        '--compare',
        nargs='+',
        type=str,
        default=None,
        help='Compare multiple result files'
    )

    parser.add_argument(
        '--labels',
        nargs='+',
        type=str,
        default=None,
        help='Labels for comparison plots'
    )

    args = parser.parse_args()

    output_manager = OutputManager(Path("output"), "lista1_monopoly")

    # Comparison mode
    if args.compare:
        filepaths = [Path(f) for f in args.compare]

        # Generate labels if not provided
        if args.labels:
            labels = args.labels
        else:
            labels = [f"Simulation {i+1}" for i in range(len(filepaths))]

        # Set output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = output_manager.get_plot_path("comparison.png")

        print("=" * 60)
        print("COMPARING SIMULATIONS")
        print("=" * 60)
        for filepath, label in zip(filepaths, labels):
            print(f"  {label}: {filepath}")
        print("=" * 60)

        compare_simulations(filepaths, labels, output_path)

    # Single visualization mode
    else:
        # Determine input file
        if args.input:
            input_path = Path(args.input)
        else:
            # Try to find most recent results file
            data_files = output_manager.list_files("results_*.txt")
            if data_files:
                input_path = max(data_files, key=lambda p: p.stat().st_mtime)
                print(f"Using most recent results: {input_path.name}")
            else:
                print("Error: No results file found. Run simulation first.")
                print("  python monopoly_simulation.py --rolls 1000000")
                sys.exit(1)

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            # Generate output name based on input
            output_name = input_path.stem + "_plot.png"
            output_path = output_manager.get_plot_path(output_name)

        print("=" * 60)
        print("VISUALIZING MONOPOLY RESULTS")
        print("=" * 60)
        print(f"Input: {input_path}")
        print(f"Output: {output_path}")
        print("=" * 60)

        visualize_results(input_path, output_path)

    print("\n✓ Visualization complete!")


if __name__ == "__main__":
    main()
