"""Plotting utilities for physics simulations

Centralized plotting functionality to avoid code duplication.
All matplotlib configuration and common plot types are defined here.

Why this is necessary:
- The same plotting code was repeated 10+ times across projects
- Ensures consistent visual style across all simulations
- Makes it easy to update all plots by changing one file
- Reduces code maintenance burden
"""

from typing import List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def setup_matplotlib(style: str = 'default') -> None:
    """Configure matplotlib with consistent settings.

    Args:
        style: Matplotlib style name (default, seaborn, ggplot, etc.)

    Why needed: Ensures all plots have consistent appearance
    """
    plt.style.use(style)
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10


def save_plot(filename: Union[str, Path], dpi: int = 300, bbox_inches: str = 'tight') -> None:
    """Save current plot to file with high quality settings.

    Args:
        filename: Output file path
        dpi: Dots per inch (resolution)
        bbox_inches: Bounding box setting ('tight' removes whitespace)

    Why needed: Consistent high-quality output across all projects
    """
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"✓ Plot saved to: {filepath}")


class Plotter:
    """Reusable plotting utilities for common visualization tasks.

    Why this class exists:
    - Eliminates duplicated plotting code across 8 projects
    - Provides consistent API for common plot types
    - Easier to maintain and extend
    """

    @staticmethod
    def plot_histogram(
        data: Union[List, np.ndarray],
        bins: int = 50,
        title: str = "Histogram",
        xlabel: str = "Value",
        ylabel: str = "Frequency",
        output_file: Optional[Path] = None
    ) -> None:
        """Create histogram with consistent styling.

        Args:
            data: Data to plot
            bins: Number of histogram bins
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            output_file: If provided, save to this file
        """
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=bins, alpha=0.7, edgecolor='black')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)

        if output_file:
            save_plot(output_file)
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plot_line(
        x: Union[List, np.ndarray],
        y: Union[List, np.ndarray],
        title: str = "Line Plot",
        xlabel: str = "X",
        ylabel: str = "Y",
        label: Optional[str] = None,
        output_file: Optional[Path] = None,
        **kwargs
    ) -> None:
        """Create line plot with consistent styling.

        Args:
            x: X-axis data
            y: Y-axis data
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            label: Line label for legend
            output_file: If provided, save to this file
            **kwargs: Additional arguments passed to plt.plot()
        """
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label=label, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)

        if label:
            plt.legend()

        if output_file:
            save_plot(output_file)
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plot_scatter(
        x: Union[List, np.ndarray],
        y: Union[List, np.ndarray],
        title: str = "Scatter Plot",
        xlabel: str = "X",
        ylabel: str = "Y",
        output_file: Optional[Path] = None,
        **kwargs
    ) -> None:
        """Create scatter plot with consistent styling.

        Args:
            x: X-axis data
            y: Y-axis data
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            output_file: If provided, save to this file
            **kwargs: Additional arguments passed to plt.scatter()
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)

        if output_file:
            save_plot(output_file)
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plot_loglog(
        x: Union[List, np.ndarray],
        y: Union[List, np.ndarray],
        title: str = "Log-Log Plot",
        xlabel: str = "X",
        ylabel: str = "Y",
        fit_line: bool = False,
        output_file: Optional[Path] = None,
        **kwargs
    ) -> Optional[Tuple[float, float]]:
        """Create log-log plot (useful for power laws like Zipf).

        Args:
            x: X-axis data
            y: Y-axis data
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            fit_line: If True, fit and plot power law
            output_file: If provided, save to this file
            **kwargs: Additional arguments passed to plt.plot()

        Returns:
            If fit_line=True, returns (slope, intercept) of fitted line

        Why needed: Lista4_Zipf uses this pattern
        """
        plt.figure(figsize=(10, 6))
        plt.loglog(x, y, 'o', label='Data', **kwargs)

        result = None
        if fit_line:
            # Fit power law: y = a * x^b  =>  log(y) = log(a) + b*log(x)
            log_x = np.log(x)
            log_y = np.log(y)
            coeffs = np.polyfit(log_x, log_y, 1)
            slope, intercept = coeffs[0], coeffs[1]

            # Plot fitted line
            y_fit = np.exp(intercept) * x ** slope
            plt.loglog(x, y_fit, 'r-', label=f'Fit: y = {np.exp(intercept):.2f} * x^{slope:.2f}')
            result = (slope, intercept)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3, which='both')
        plt.legend()

        if output_file:
            save_plot(output_file)
        else:
            plt.show()
        plt.close()

        return result

    @staticmethod
    def plot_heatmap(
        data: np.ndarray,
        title: str = "Heatmap",
        xlabel: str = "X",
        ylabel: str = "Y",
        cmap: str = 'viridis',
        output_file: Optional[Path] = None
    ) -> None:
        """Create heatmap visualization.

        Args:
            data: 2D array to visualize
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            cmap: Colormap name
            output_file: If provided, save to this file

        Why needed: Useful for cellular automata and cluster growth
        """
        plt.figure(figsize=(10, 8))
        plt.imshow(data, cmap=cmap, interpolation='nearest')
        plt.colorbar(label='Value')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        if output_file:
            save_plot(output_file)
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plot_multiple_lines(
        data_list: List[Tuple[np.ndarray, np.ndarray, str]],
        title: str = "Multiple Lines",
        xlabel: str = "X",
        ylabel: str = "Y",
        output_file: Optional[Path] = None
    ) -> None:
        """Plot multiple lines on same axes.

        Args:
            data_list: List of (x, y, label) tuples
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            output_file: If provided, save to this file

        Why needed: Comparing different simulation runs
        """
        plt.figure(figsize=(10, 6))

        for x, y, label in data_list:
            plt.plot(x, y, label=label)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend()

        if output_file:
            save_plot(output_file)
        else:
            plt.show()
        plt.close()


# Convenience function for backward compatibility
def plot_simple(
    y: Union[List, np.ndarray],
    title: str = "",
    xlabel: str = "Index",
    ylabel: str = "Value"
) -> None:
    """Simple quick plot for debugging.

    Args:
        y: Y-axis data (x will be indices)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    x = np.arange(len(y))
    Plotter.plot_line(x, y, title=title, xlabel=xlabel, ylabel=ylabel)
