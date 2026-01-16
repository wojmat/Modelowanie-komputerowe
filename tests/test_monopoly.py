"""Tests for Lista1 Monopoly simulation"""

import pytest
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lista1_monopoly.monopoly_simulation import Board, MonopolySimulation, MonopolyConfig


def test_board_creation():
    """Test board initialization."""
    board = Board(num_squares=40)

    assert board.num_squares == 40
    assert len(board.visit_counts) == 40
    assert np.all(board.visit_counts == 0)


def test_board_visit_recording():
    """Test recording visits."""
    board = Board(num_squares=40)

    board.record_visit(0)
    board.record_visit(0)
    board.record_visit(5)

    assert board.visit_counts[0] == 2
    assert board.visit_counts[5] == 1
    assert board.visit_counts[10] == 0


def test_board_wraparound():
    """Test position wrapping."""
    board = Board(num_squares=40)

    board.record_visit(45)  # Should wrap to 5
    assert board.visit_counts[5] == 1


def test_simulation_dice_roll():
    """Test dice rolling."""
    config = MonopolyConfig(num_squares=40, random_seed=42)
    sim = MonopolySimulation(
        num_squares=40,
        random_seed=42
    )

    die1, die2 = sim.roll_dice()

    assert 1 <= die1 <= 6
    assert 1 <= die2 <= 6


def test_simulation_reproducibility():
    """Test that same seed gives same results."""
    config = MonopolyConfig(num_rolls=100, random_seed=42)

    sim1 = MonopolySimulation(num_squares=40, random_seed=42)
    board1 = sim1.run(100, verbose=False)

    sim2 = MonopolySimulation(num_squares=40, random_seed=42)
    board2 = sim2.run(100, verbose=False)

    np.testing.assert_array_equal(board1.visit_counts, board2.visit_counts)


def test_probability_sum():
    """Test that probabilities sum to ~100%."""
    sim = MonopolySimulation(num_squares=40, random_seed=42)
    board = sim.run(1000, verbose=False)

    probs = board.get_probabilities(1000)
    total_prob = np.sum(probs)

    # Should sum to 100% within rounding error
    assert abs(total_prob - 100.0) < 0.01
