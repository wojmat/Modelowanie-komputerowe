"""Tests for common utilities"""

import pytest
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from common.utils import (
    validate_positive,
    validate_range,
    safe_divide,
    normalize_array,
    moving_average
)


def test_validate_positive():
    """Test positive value validation."""
    # Should pass
    validate_positive(1, "test")
    validate_positive(0.1, "test")
    validate_positive(1000, "test")

    # Should raise
    with pytest.raises(ValueError):
        validate_positive(0, "test")

    with pytest.raises(ValueError):
        validate_positive(-1, "test")


def test_validate_range():
    """Test range validation."""
    # Should pass
    validate_range(0.5, 0.0, 1.0, "test")
    validate_range(0, 0, 1, "test")
    validate_range(1, 0, 1, "test")

    # Should raise
    with pytest.raises(ValueError):
        validate_range(1.5, 0.0, 1.0, "test")

    with pytest.raises(ValueError):
        validate_range(-0.1, 0.0, 1.0, "test")


def test_safe_divide():
    """Test safe division."""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(10, 0, default=999) == 999

    # Array division
    result = safe_divide(np.array([1, 2, 3]), np.array([2, 0, 3]))
    expected = np.array([0.5, 0.0, 1.0])
    np.testing.assert_array_equal(result, expected)


def test_normalize_array():
    """Test array normalization."""
    arr = np.array([10, 20, 30])
    normalized = normalize_array(arr)

    assert normalized[0] == 0.0
    assert normalized[1] == 0.5
    assert normalized[2] == 1.0

    # Constant array
    const_arr = np.array([5, 5, 5])
    normalized_const = normalize_array(const_arr)
    np.testing.assert_array_equal(normalized_const, np.zeros(3))


def test_moving_average():
    """Test moving average calculation."""
    data = np.array([1, 2, 3, 4, 5])

    # Window size 1 (no smoothing)
    result1 = moving_average(data, 1)
    np.testing.assert_array_equal(result1, data)

    # Window size 2
    result2 = moving_average(data, 2)
    expected2 = np.array([1.5, 2.5, 3.5, 4.5])
    np.testing.assert_array_equal(result2, expected2)
