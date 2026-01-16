"""Population analysis for Zipf's Law

Analyzes city/country populations to test Zipf's Law in a different domain.

Why Zipf's Law applies to populations:
- Preferential attachment: Large cities attract more migrants
- Economic networks: Trade favors larger population centers
- Historical path dependence: Early settlements grew larger

This is the same power-law mechanism as word frequencies,
but in a completely different system - showing universality.
"""

from typing import List, Tuple, Optional
from pathlib import Path
import numpy as np
import sys

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from .zipf_fitter import ZipfFitter, ZipfFitResult, plot_zipf_law
from common.config import OutputManager


class PopulationAnalyzer:
    """Analyzes population data for Zipf's Law.

    Why separate class?
    - Different data format from text
    - Specific parsing logic for population files
    - Can extend to handle different data sources (CSV, API, etc.)
    """

    def __init__(self, filepath: Path, encoding: str = 'utf-8'):
        """Initialize population analyzer.

        Args:
            filepath: Path to population data file
            encoding: File encoding

        Expected file format:
            City Name 1000000
            Another City 500000
            Third City 250000
            ...

        (City name can have spaces, population is last token)
        """
        self.filepath = Path(filepath)
        self.encoding = encoding

        self.cities: List[str] = []
        self.populations: List[int] = []

        self._load_data()

    def _load_data(self) -> None:
        """Load and parse population data.

        Why separate method?
        - Error handling in one place
        - Easy to extend to different formats
        - Validation logic isolated
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"Population file not found: {self.filepath}")

        with open(self.filepath, 'r', encoding=self.encoding) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                parts = line.split()
                if len(parts) < 2:
                    print(f"Warning: Skipping malformed line {line_num}: {line}")
                    continue

                # Last token is population, rest is city name
                city_name = ' '.join(parts[:-1])
                population_str = parts[-1]

                try:
                    # Remove commas from numbers (e.g., "1,000,000" → "1000000")
                    population = int(population_str.replace(',', '').replace(' ', ''))

                    self.cities.append(city_name)
                    self.populations.append(population)

                except ValueError:
                    print(f"Warning: Could not parse line {line_num}: {line}")
                    continue

        if not self.cities:
            raise ValueError(f"No valid data found in {self.filepath}")

        # Sort by population (descending) to ensure ranks are correct
        sorted_pairs = sorted(
            zip(self.cities, self.populations),
            key=lambda x: x[1],
            reverse=True
        )

        self.cities, self.populations = zip(*sorted_pairs)
        self.cities = list(self.cities)
        self.populations = list(self.populations)

    def get_ranks_and_populations(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get ranks and populations as arrays.

        Returns:
            Tuple of (ranks, populations)
        """
        ranks = np.arange(1, len(self.cities) + 1)
        pops = np.array(self.populations)
        return ranks, pops

    def get_statistics(self) -> dict:
        """Calculate population statistics.

        Returns:
            Dictionary with stats
        """
        pops = np.array(self.populations)

        return {
            'num_cities': len(self.cities),
            'largest_city': self.cities[0] if self.cities else None,
            'largest_population': self.populations[0] if self.populations else 0,
            'smallest_city': self.cities[-1] if self.cities else None,
            'smallest_population': self.populations[-1] if self.populations else 0,
            'total_population': int(np.sum(pops)),
            'mean_population': float(np.mean(pops)),
            'median_population': float(np.median(pops)),
        }

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return (
            f"PopulationAnalyzer({self.filepath.name})\n"
            f"  Cities: {stats['num_cities']}\n"
            f"  Largest: {stats['largest_city']} ({stats['largest_population']:,})\n"
            f"  Total population: {stats['total_population']:,}"
        )


def main():
    """Command-line interface for population analysis.

    Example:
        python population_analysis.py cities.txt
        python population_analysis.py cities.txt --output cities_zipf.png
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze city/country populations for Zipf's Law",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'file',
        type=str,
        help='Population data file'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output plot file'
    )

    parser.add_argument(
        '--encoding',
        type=str,
        default='utf-8',
        help='File encoding'
    )

    args = parser.parse_args()

    # Load data
    print("=" * 70)
    print("POPULATION ZIPF'S LAW ANALYSIS")
    print("=" * 70)

    filepath = Path(args.file)
    analyzer = PopulationAnalyzer(filepath, encoding=args.encoding)

    print(f"\n{analyzer}")

    stats = analyzer.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total population: {stats['total_population']:,}")
    print(f"  Mean population: {stats['mean_population']:,.0f}")
    print(f"  Median population: {stats['median_population']:,.0f}")

    # Fit Zipf's law
    print("\nFitting Zipf's law...")
    fitter = ZipfFitter()
    ranks, pops = analyzer.get_ranks_and_populations()
    result = fitter.fit(ranks, pops, source_name=filepath.stem)

    print(f"\n{result}")

    # Interpret results
    print("\nInterpretation:")
    if 0.9 <= result.alpha <= 1.1:
        print("  ✓ Excellent fit to Zipf's law (α ≈ 1.0)")
    elif 0.8 <= result.alpha <= 1.2:
        print("  ✓ Good fit to power law")
    else:
        print(f"  ⚠ Deviation from Zipf's law (α = {result.alpha:.3f})")

    if result.r_squared > 0.95:
        print("  ✓ Very high R² - strong power-law relationship")
    elif result.r_squared > 0.85:
        print("  ✓ Good R² - clear power-law trend")
    else:
        print("  ⚠ Lower R² - other factors may be important")

    # Plot
    output_path = Path(args.output) if args.output else None

    if output_path is None:
        om = OutputManager(Path("output"), "lista4_zipf")
        output_path = om.get_plot_path(f"{filepath.stem}_zipf.png")

    plot_zipf_law(
        [result],
        output_path=output_path,
        title=f"Zipf's Law: {filepath.stem} Population Distribution"
    )

    print(f"\n✓ Analysis complete! Plot saved to: {output_path}")


if __name__ == "__main__":
    main()
