"""Lista 3: Conway's Game of Life

This module implements Conway's Game of Life cellular automaton with
statistical analysis of how initial density and grid size affect long-term behavior.

Physics concept: Self-organization and emergent complexity from simple rules
"""

from .simulation import GameOfLifeSimulation, GameOfLifeGrid
from .visualizer import GameOfLifeVisualizer
from .experiments import run_density_experiments, analyze_convergence

__all__ = [
    'GameOfLifeSimulation',
    'GameOfLifeGrid',
    'GameOfLifeVisualizer',
    'run_density_experiments',
    'analyze_convergence',
]
