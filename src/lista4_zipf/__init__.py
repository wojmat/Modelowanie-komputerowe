"""Lista 4: Zipf's Law Analysis

This module analyzes Zipf's Law in natural language and city populations.
Zipf's Law states that frequency is inversely proportional to rank.

Physics concept: Power-law distributions in complex systems
"""

from .text_analysis import TextAnalyzer, analyze_multiple_texts
from .population_analysis import PopulationAnalyzer
from .zipf_fitter import ZipfFitter

__all__ = [
    'TextAnalyzer',
    'analyze_multiple_texts',
    'PopulationAnalyzer',
    'ZipfFitter',
]
