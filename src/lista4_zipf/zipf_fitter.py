"""Zipf's Law fitting and statistical analysis

This module fits power-law distributions to rank-frequency data and
provides statistical validation of Zipf's Law.

Why separate from text analysis?
- Single Responsibility Principle
- Can fit Zipf's law to any ranked data (cities, websites, etc.)
- Reusable across different domains
- Statistical methods isolated from data collection

Power-law fitting:
    f(r) = C * r^(-α)

In log-log space, this is linear:
    log(f) = log(C) - α * log(r)

We can use linear regression on log-transformed data.

Statistical tests:
1. R² (coefficient of determination) - how well does line fit?
2. Kolmogorov-Smirnov test - is data power-law distributed?
3. Residual analysis - systematic deviations from power law?
"""

from typing import Tuple, Dict, Optional
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from dataclasses import dataclass
import sys

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from .text_analysis import TextAnalyzer, analyze_multiple_texts
from common.plotting import save_plot


@dataclass
class ZipfFitResult:
    """Container for Zipf's law fitting results.

    Why dataclass?
    - Clean API for results
    - Type hints
    - Easy to serialize
    """
    C: float  # Constant in f(r) = C * r^(-α)
    alpha: float  # Zipf exponent (typically ~1.0 for natural language)
    r_squared: float  # Goodness of fit (0-1, higher is better)

    # Raw data
    ranks: np.ndarray
    observed_frequencies: np.ndarray
    fitted_frequencies: np.ndarray

    # Optional metadata
    source_name: str = "Unknown"

    def get_formula_string(self) -> str:
        """Get human-readable formula string.

        Returns:
            LaTeX-formatted formula
        """
        return f"$f(r) = {self.C:.2f} \\times r^{{-{self.alpha:.3f}}}$"

    def __repr__(self) -> str:
        return (
            f"ZipfFitResult(source={self.source_name})\n"
            f"  α = {self.alpha:.4f} (Zipf exponent)\n"
            f"  C = {self.C:.2f} (constant)\n"
            f"  R² = {self.r_squared:.4f} (goodness of fit)"
        )


class ZipfFitter:
    """Fits power-law distributions to ranked data.

    Why a class?
    - Encapsulates fitting algorithm
    - Can add different fitting methods (MLE, likelihood ratio test)
    - Maintains fit results for analysis
    """

    def __init__(self, min_rank: int = 1, max_rank: Optional[int] = None):
        """Initialize fitter.

        Args:
            min_rank: Minimum rank to include in fit
            max_rank: Maximum rank to include (None = all)

        Why rank filtering?
        - Very rare words (high rank) are noisy
        - Sometimes want to fit only high-frequency words
        - Allows testing if Zipf holds across full range
        """
        self.min_rank = min_rank
        self.max_rank = max_rank

    def fit(
        self,
        ranks: np.ndarray,
        frequencies: np.ndarray,
        source_name: str = "Unknown"
    ) -> ZipfFitResult:
        """Fit Zipf's law to rank-frequency data.

        Args:
            ranks: Rank values (1, 2, 3, ...)
            frequencies: Observed frequencies
            source_name: Name of data source (for labeling)

        Returns:
            ZipfFitResult with fit parameters

        Why log-log regression?
        - Power law is linear in log-log space
        - Simple least squares gives good estimate
        - More sophisticated: Maximum Likelihood Estimation
          (but requires more code, similar results for clean data)
        """
        # Filter ranks
        if self.max_rank is None:
            mask = ranks >= self.min_rank
        else:
            mask = (ranks >= self.min_rank) & (ranks <= self.max_rank)

        ranks_filtered = ranks[mask]
        freqs_filtered = frequencies[mask]

        if len(ranks_filtered) < 2:
            raise ValueError("Not enough data points for fitting")

        # Log-log transform
        log_ranks = np.log(ranks_filtered)
        log_freqs = np.log(freqs_filtered)

        # Linear regression in log-log space
        # log(f) = log(C) - α * log(r)
        # This is y = intercept + slope * x
        coefficients = np.polyfit(log_ranks, log_freqs, deg=1)
        slope = coefficients[0]
        intercept = coefficients[1]

        # Extract Zipf parameters
        alpha = -slope  # Zipf exponent
        C = np.exp(intercept)  # Constant

        # Calculate fitted values
        fitted_freqs = C * ranks ** (-alpha)

        # Calculate R² (goodness of fit)
        # R² = 1 - (SS_residual / SS_total)
        log_fitted = np.log(fitted_freqs[mask])
        ss_residual = np.sum((log_freqs - log_fitted) ** 2)
        ss_total = np.sum((log_freqs - np.mean(log_freqs)) ** 2)
        r_squared = 1 - (ss_residual / ss_total)

        return ZipfFitResult(
            C=C,
            alpha=alpha,
            r_squared=r_squared,
            ranks=ranks,
            observed_frequencies=frequencies,
            fitted_frequencies=fitted_freqs,
            source_name=source_name
        )

    def fit_text_analyzer(self, analyzer: TextAnalyzer) -> ZipfFitResult:
        """Fit Zipf's law to TextAnalyzer results.

        Args:
            analyzer: TextAnalyzer with processed text

        Returns:
            ZipfFitResult

        Why convenience method?
        - Common use case: fit to text analysis
        - Cleaner API than extracting ranks/freqs manually
        """
        ranks, freqs = analyzer.get_ranks_and_frequencies()
        return self.fit(ranks, freqs, source_name=analyzer.filepath.stem)


def plot_zipf_law(
    fit_results: list[ZipfFitResult],
    output_path: Optional[Path] = None,
    title: str = "Zipf's Law Analysis"
) -> None:
    """Create publication-quality Zipf's law plot.

    Args:
        fit_results: List of fit results to plot
        output_path: Where to save (None = display)
        title: Plot title

    Why separate plotting?
    - Separation of concerns: analysis vs visualization
    - Can customize plots without changing fitting code
    - Easy to create different plot styles
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    colors = plt.cm.tab10(np.linspace(0, 1, len(fit_results)))

    # Plot 1: Log-log plot with fits
    for result, color in zip(fit_results, colors):
        # Observed data
        ax1.loglog(
            result.ranks,
            result.observed_frequencies,
            'o',
            color=color,
            alpha=0.6,
            markersize=4,
            label=f'{result.source_name} (data)'
        )

        # Fitted line
        ax1.loglog(
            result.ranks,
            result.fitted_frequencies,
            '--',
            color=color,
            linewidth=2,
            label=f'{result.source_name} fit: α={result.alpha:.3f}, R²={result.r_squared:.3f}'
        )

    ax1.set_xlabel('Rank', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Zipf\'s Law: Log-Log Plot', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3, which='both')

    # Plot 2: Zipf exponents comparison
    names = [r.source_name for r in fit_results]
    alphas = [r.alpha for r in fit_results]
    r_squareds = [r.r_squared for r in fit_results]

    x_pos = np.arange(len(names))

    bars = ax2.bar(x_pos, alphas, color=colors, alpha=0.7, edgecolor='black')

    # Add R² values as text on bars
    for i, (bar, r2) in enumerate(zip(bars, r_squareds)):
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'R²={r2:.3f}',
            ha='center',
            va='bottom',
            fontsize=9
        )

    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Ideal Zipf (α=1.0)')
    ax2.set_xlabel('Text Source', fontsize=12)
    ax2.set_ylabel('Zipf Exponent (α)', fontsize=12)
    ax2.set_title('Zipf Exponents Comparison', fontsize=14, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(names, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim(0, max(alphas) * 1.2)

    plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    if output_path:
        save_plot(output_path)
    else:
        plt.show()

    plt.close()


def main():
    """Command-line interface for Zipf's law fitting.

    Example:
        python zipf_fitter.py text1.txt text2.txt text3.txt
        python zipf_fitter.py *.txt --output plot.png
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Fit Zipf's law to text data",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'files',
        nargs='+',
        type=str,
        help='Text files to analyze'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output plot file (default: display)'
    )

    parser.add_argument(
        '--min-rank',
        type=int,
        default=1,
        help='Minimum rank to include in fit'
    )

    parser.add_argument(
        '--max-rank',
        type=int,
        default=None,
        help='Maximum rank to include in fit'
    )

    args = parser.parse_args()

    # Analyze texts
    print("Analyzing texts...")
    filepaths = [Path(f) for f in args.files]
    analyzers = analyze_multiple_texts(filepaths, verbose=True)

    if not analyzers:
        print("No texts successfully analyzed.")
        sys.exit(1)

    # Fit Zipf's law
    print("\nFitting Zipf's law...")
    fitter = ZipfFitter(min_rank=args.min_rank, max_rank=args.max_rank)
    fit_results = []

    for analyzer in analyzers:
        result = fitter.fit_text_analyzer(analyzer)
        print(f"\n{result}")
        fit_results.append(result)

    # Plot
    output_path = Path(args.output) if args.output else None

    from common.config import OutputManager
    if output_path is None:
        om = OutputManager(Path("output"), "lista4_zipf")
        output_path = om.get_plot_path("zipf_analysis.png")

    plot_zipf_law(fit_results, output_path=output_path)

    print(f"\n✓ Analysis complete! Plot saved to: {output_path}")


if __name__ == "__main__":
    main()
