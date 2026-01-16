# Test Suite

Basic unit tests for computational physics simulations.

## Running Tests

### Install pytest

```bash
pip install pytest
```

### Run all tests

```bash
# From repository root
pytest tests/

# With verbose output
pytest tests/ -v

# With coverage
pip install pytest-cov
pytest tests/ --cov=src
```

### Run specific test file

```bash
pytest tests/test_common_utils.py -v
pytest tests/test_monopoly.py -v
```

## Test Coverage

Current tests cover:
- ✅ Common utilities (validation, safe operations)
- ✅ Lista1 Monopoly (board, dice, reproducibility)
- ⚠️ Other projects: Basic smoke tests recommended

## Adding New Tests

Create test files following pattern:

```python
# tests/test_<module>.py

import pytest
from src.<module> import SomeClass

def test_something():
    """Test description."""
    obj = SomeClass()
    assert obj.method() == expected_value
```

## Best Practices

1. **Test one thing per test**: Clear failure messages
2. **Use descriptive names**: `test_board_wraparound` not `test1`
3. **Test edge cases**: Zero, negative, boundary values
4. **Use fixtures**: Share setup code
5. **Mock external dependencies**: Don't hit real files/network

## Future Tests

Recommended additions:
- Game of Life: Pattern detection, Conway's rules
- Zipf's Law: Power-law fitting, R² calculation
- N-Body: Energy conservation, integrator comparison
- Random Walks: Mean squared displacement, diffusion

## Example Test Structure

```python
import pytest
import numpy as np

class TestGameOfLife:
    @pytest.fixture
    def small_grid(self):
        """Create 10x10 test grid."""
        from lista3_game_of_life import GameOfLifeGrid
        return GameOfLifeGrid(size=10, initial_density=0.3, random_seed=42)

    def test_density(self, small_grid):
        """Test density calculation."""
        density = small_grid.get_density()
        assert 0.0 <= density <= 1.0

    def test_update_preserves_size(self, small_grid):
        """Test grid size unchanged after update."""
        original_size = small_grid.size
        # ... update logic ...
        assert small_grid.size == original_size
```
