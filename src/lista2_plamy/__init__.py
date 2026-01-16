"""Lista 2: Plamy (Pattern Growth) - Cellular Automaton

This module implements a cellular automaton that grows patterns from random
initial conditions based on neighbor counting rules.

Physics concept: Pattern formation in discrete dynamical systems
"""

from .simulation import PlamySimulation, PlamyGrid
from .visualizer import PlamyVisualizer

__all__ = ['PlamySimulation', 'PlamyGrid', 'PlamyVisualizer']
