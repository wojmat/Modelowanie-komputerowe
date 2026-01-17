"""General utility functions for physics simulations

Common helper functions used across multiple projects.

Why this module exists:
- Eliminate duplicated validation code
- Provide consistent error messages
- Centralize file operations
- Type-safe utility functions
"""

from pathlib import Path
from typing import Union, Tuple, Optional
import numpy as np


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if necessary.

    Args:
        path: Directory path

    Returns:
        Path object to directory

    Why needed: Original code had no error handling for missing directories

    Example:
        >>> ensure_dir("output/plots")
        Path("output/plots")
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_positive(value: Union[int, float], name: str = "value") -> None:
    """Validate that a value is positive.

    Args:
        value: Value to check
        name: Parameter name for error message

    Raises:
        ValueError: If value is not positive

    Why needed: Prevents invalid parameters (negative grid size, etc.)

    Example:
        >>> validate_positive(10, "grid_size")  # OK
        >>> validate_positive(-5, "grid_size")  # Raises ValueError
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got: {value}")


def validate_range(
    value: Union[int, float],
    min_val: Union[int, float],
    max_val: Union[int, float],
    name: str = "value"
) -> None:
    """Validate that a value is within specified range.

    Args:
        value: Value to check
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        name: Parameter name for error message

    Raises:
        ValueError: If value is outside range

    Why needed: Validate probabilities, densities, etc.

    Example:
        >>> validate_range(0.5, 0.0, 1.0, "density")  # OK
        >>> validate_range(1.5, 0.0, 1.0, "density")  # Raises ValueError
    """
    if not (min_val <= value <= max_val):
        raise ValueError(
            f"{name} must be in [{min_val}, {max_val}], got: {value}"
        )


def safe_divide(
    numerator: Union[float, np.ndarray],
    denominator: Union[float, np.ndarray],
    default: float = 0.0
) -> Union[float, np.ndarray]:
    """Safely divide, handling division by zero.

    Args:
        numerator: Numerator value(s)
        denominator: Denominator value(s)
        default: Value to return when dividing by zero

    Returns:
        Result of division, or default where denominator is zero

    Why needed: Prevent crashes in density calculations, averages, etc.

    Example:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)
        0.0
        >>> safe_divide(np.array([1, 2, 3]), np.array([2, 0, 3]))
        array([0.5, 0.0, 1.0])
    """
    if isinstance(denominator, np.ndarray):
        result = np.full_like(numerator, default, dtype=float)
        mask = denominator != 0
        result[mask] = numerator[mask] / denominator[mask]
        return result
    else:
        return numerator / denominator if denominator != 0 else default


def format_time(seconds: float) -> str:
    """Format seconds as human-readable time string.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted string (e.g., "2h 34m 56s")

    Why needed: Better user feedback for long simulations

    Example:
        >>> format_time(150)
        "2m 30s"
        >>> format_time(7384)
        "2h 3m 4s"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def print_progress(
    current: int,
    total: int,
    prefix: str = "Progress",
    bar_length: int = 40
) -> None:
    """Print progress bar to console.

    Args:
        current: Current iteration
        total: Total iterations
        prefix: Text to display before progress bar
        bar_length: Length of progress bar in characters

    Why needed: Provide feedback during long simulations

    Example:
        >>> for i in range(100):
        ...     print_progress(i+1, 100, "Simulating")
        Simulating: [████████████████████] 100.0% (100/100)
    """
    percent = 100.0 * current / total
    filled = int(bar_length * current / total)
    bar = '█' * filled + '-' * (bar_length - filled)
    print(f'\r{prefix}: [{bar}] {percent:.1f}% ({current}/{total})', end='')

    if current == total:
        print()  # New line when complete


def calculate_statistics(data: np.ndarray) -> dict:
    """Calculate basic statistical measures.

    Args:
        data: Input data array

    Returns:
        Dictionary with mean, std, min, max, median

    Why needed: Consistent statistics across all projects

    Example:
        >>> data = np.array([1, 2, 3, 4, 5])
        >>> stats = calculate_statistics(data)
        >>> stats['mean']
        3.0
    """
    return {
        'mean': np.mean(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'median': np.median(data),
    }


def estimate_memory(array_shape: Tuple[int, ...], dtype=np.float64) -> str:
    """Estimate memory usage of numpy array.

    Args:
        array_shape: Shape of array
        dtype: Data type of array elements

    Returns:
        Human-readable memory size (e.g., "4.5 MB")

    Why needed: Warn users about large memory allocations

    Example:
        >>> estimate_memory((1000, 1000), np.float64)
        "7.6 MB"
    """
    num_elements = np.prod(array_shape)
    bytes_per_element = np.dtype(dtype).itemsize
    total_bytes = num_elements * bytes_per_element

    # Convert to human-readable format
    for unit in ['B', 'KB', 'MB', 'GB']:
        if total_bytes < 1024.0:
            return f"{total_bytes:.1f} {unit}"
        total_bytes /= 1024.0

    return f"{total_bytes:.1f} TB"


def set_random_seed(seed: Optional[int] = None) -> int:
    """Set random seed for reproducibility.

    Args:
        seed: Random seed value (if None, uses current time)

    Returns:
        The seed value that was set

    Why needed: Reproducible simulations for scientific validation

    Example:
        >>> set_random_seed(42)
        42
        >>> np.random.rand()  # Same result every time
        0.3745401188473625
    """
    if seed is None:
        import time
        seed = int(time.time())

    np.random.seed(seed)

    # Also seed Python's random module if imported
    try:
        import random
        random.seed(seed)
    except ImportError:
        pass

    return seed


def normalize_array(arr: np.ndarray) -> np.ndarray:
    """Normalize array to [0, 1] range.

    Args:
        arr: Input array

    Returns:
        Normalized array

    Why needed: Visualization, probability normalization

    Example:
        >>> arr = np.array([10, 20, 30])
        >>> normalize_array(arr)
        array([0., 0.5, 1.])
    """
    min_val = np.min(arr)
    max_val = np.max(arr)

    if max_val == min_val:
        return np.zeros_like(arr, dtype=float)

    return (arr - min_val) / (max_val - min_val)


def moving_average(data: np.ndarray, window_size: int) -> np.ndarray:
    """Calculate moving average of data.

    Args:
        data: Input data
        window_size: Size of moving window

    Returns:
        Smoothed data array

    Why needed: Smooth noisy simulation data for clearer plots

    Example:
        >>> data = np.array([1, 2, 3, 4, 5])
        >>> moving_average(data, 2)
        array([1.5, 2.5, 3.5, 4.5])
    """
    if window_size <= 1:
        return data

    cumsum = np.cumsum(data)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    return cumsum[window_size - 1:] / window_size


class Timer:
    """Simple context manager for timing code blocks.

    Why needed: Measure performance of simulation components

    Example:
        >>> with Timer("Simulation"):
        ...     # Run simulation
        ...     pass
        Simulation took: 5.23s
    """

    def __init__(self, name: str = "Operation", silent: bool = False):
        """Initialize timer.

        Args:
            name: Name of operation being timed
            silent: If True, don't print timing results
        """
        self.name = name
        self.silent = silent
        self.start_time = None
        self.elapsed = None

    def __enter__(self):
        """Start timing."""
        import time
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        """Stop timing and print result."""
        import time
        self.elapsed = time.time() - self.start_time
        if not self.silent:
            print(f"{self.name} took: {format_time(self.elapsed)}")

    def get_elapsed(self) -> float:
        """Get elapsed time in seconds.

        Returns:
            Elapsed time in seconds
        """
        return self.elapsed if self.elapsed is not None else 0.0
