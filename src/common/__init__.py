"""Common utilities for physics simulations

This module provides shared functionality used across multiple projects:
- Plotting utilities
- Configuration management
- File I/O helpers
- Mathematical utilities
"""

from .plotting import Plotter, save_plot, setup_matplotlib
from .config import Config, OutputManager
from .utils import ensure_dir, validate_positive, validate_range

__all__ = [
    'Plotter',
    'save_plot',
    'setup_matplotlib',
    'Config',
    'OutputManager',
    'ensure_dir',
    'validate_positive',
    'validate_range',
]
