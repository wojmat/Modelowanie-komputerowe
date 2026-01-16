"""Lista 1: Monopoly Board Simulation

This module simulates random movement on a Monopoly board using dice rolls
and analyzes the probability distribution of landing on each square.

Physics concept: Discrete random walk on periodic domain
"""

from .monopoly_simulation import MonopolySimulation, Board
from .visualize import visualize_results

__all__ = ['MonopolySimulation', 'Board', 'visualize_results']
