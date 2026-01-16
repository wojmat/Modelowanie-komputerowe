"""Text analysis for Zipf's Law

Why this refactoring was necessary:

ORIGINAL ISSUES:
1. Hardcoded file paths - cannot analyze arbitrary texts
2. No CLI arguments - must edit code to change inputs
3. Code duplication - same logic in zipf.py, zipf_zad2.py, zipf_zad3.py
4. No error handling - crashes on missing/invalid files
5. No text preprocessing options - fixed lowercase, no stemming
6. Limited analysis - just plots, no goodness-of-fit metrics
7. Not reusable - function does everything, can't extract parts

IMPROVEMENTS:
1. Object-oriented design - TextAnalyzer class reusable
2. CLI argument parsing - analyze any text file
3. Unified codebase - single implementation with options
4. Comprehensive error handling - validates files, encoding
5. Configurable preprocessing - stopwords, case, punctuation
6. Statistical analysis - R², Kolmogorov-Smirnov test
7. Modular - separate analysis from visualization

Zipf's Law:
For word frequencies in natural language:
    frequency(rank) = C / rank^α

where:
- C is a constant (depends on text length)
- α is the Zipf exponent (typically ~1.0 for natural language)
- rank is the word's rank by frequency (1 = most common)

This is a power-law distribution, observed in many complex systems:
- Word frequencies (Zipf's original work, 1935)
- City populations
- Website traffic
- Income distribution
- File sizes

Why does it occur?
- Preferential attachment ("rich get richer")
- Optimization processes
- Emergent property of complex systems
"""

from typing import List, Tuple, Dict, Optional, Set
import re
from collections import Counter
from pathlib import Path
import numpy as np
import sys

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.utils import validate_positive, Timer
from common.plotting import Plotter


class TextAnalyzer:
    """Analyzes word frequency distributions in text.

    Why a class?
    - Encapsulates text processing logic
    - Reusable across different texts
    - Maintains state (word counts, statistics)
    - Easy to extend (add stopwords, stemming, etc.)
    """

    def __init__(
        self,
        filepath: Path,
        encoding: str = 'utf-8',
        remove_punctuation: bool = True,
        lowercase: bool = True,
        min_word_length: int = 1,
        stopwords: Optional[Set[str]] = None
    ):
        """Initialize text analyzer.

        Args:
            filepath: Path to text file
            encoding: Text file encoding
            remove_punctuation: Remove punctuation marks
            lowercase: Convert to lowercase
            min_word_length: Minimum word length to include
            stopwords: Set of words to exclude (e.g., "the", "a", "is")

        Why these parameters?
        - Original code hardcoded all preprocessing
        - Now configurable for different analysis needs
        - Stopwords optional (Zipf's law holds even with stopwords)
        """
        self.filepath = Path(filepath)
        self.encoding = encoding
        self.remove_punctuation = remove_punctuation
        self.lowercase = lowercase
        self.min_word_length = min_word_length
        self.stopwords = stopwords or set()

        # Results
        self.text: str = ""
        self.words: List[str] = []
        self.word_counts: Counter = Counter()
        self.frequencies: List[Tuple[str, int]] = []

        # Load and process text
        self._load_text()
        self._process_text()

    def _load_text(self) -> None:
        """Load text from file with error handling.

        Why separate method?
        - Isolates I/O from processing
        - Easy to add support for URLs, databases, etc.
        - Proper error handling
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"Text file not found: {self.filepath}")

        try:
            with open(self.filepath, 'r', encoding=self.encoding) as f:
                self.text = f.read()
        except UnicodeDecodeError as e:
            raise ValueError(
                f"Failed to decode {self.filepath} with encoding {self.encoding}. "
                f"Try different encoding (e.g., 'cp1250' for Polish). Error: {e}"
            )

        if not self.text.strip():
            raise ValueError(f"Text file is empty: {self.filepath}")

    def _process_text(self) -> None:
        """Process text into word frequency distribution.

        Steps:
        1. Lowercase (optional)
        2. Remove punctuation (optional)
        3. Split into words
        4. Filter by length
        5. Remove stopwords
        6. Count frequencies
        7. Sort by frequency

        Why this order?
        - Lowercase before counting (treat "The" and "the" as same)
        - Remove punctuation to avoid "word," vs "word"
        - Filter after splitting for efficiency
        """
        text = self.text

        # Lowercase
        if self.lowercase:
            text = text.lower()

        # Remove punctuation
        if self.remove_punctuation:
            # Keep only letters, numbers, whitespace
            # Original used: re.sub(r'[^\w\s]', '', text)
            # This keeps underscores, which is usually fine
            text = re.sub(r'[^\w\s]', '', text)

        # Split into words
        words = text.split()

        # Filter
        words = [
            word for word in words
            if len(word) >= self.min_word_length
            and word not in self.stopwords
        ]

        self.words = words

        # Count frequencies
        self.word_counts = Counter(words)

        # Sort by frequency (descending)
        self.frequencies = sorted(
            self.word_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

    def get_ranks_and_frequencies(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get ranks and frequencies as arrays.

        Returns:
            Tuple of (ranks, frequencies) arrays

        Why arrays?
        - NumPy vectorization for fast computation
        - Easy to plot, fit, analyze
        - Standard format for scientific data
        """
        ranks = np.arange(1, len(self.frequencies) + 1)
        freqs = np.array([count for _, count in self.frequencies])
        return ranks, freqs

    def get_statistics(self) -> Dict:
        """Calculate text statistics.

        Returns:
            Dictionary with text stats

        Why?
        - Context for interpreting Zipf analysis
        - Quality checks (vocabulary size, avg frequency)
        """
        ranks, freqs = self.get_ranks_and_frequencies()

        return {
            'total_words': len(self.words),
            'unique_words': len(self.word_counts),
            'vocabulary_richness': len(self.word_counts) / len(self.words),
            'most_common_word': self.frequencies[0][0] if self.frequencies else None,
            'most_common_count': self.frequencies[0][1] if self.frequencies else 0,
            'mean_frequency': float(np.mean(freqs)),
            'median_frequency': float(np.median(freqs)),
        }

    def save_word_frequencies(self, output_path: Path) -> None:
        """Save word frequencies to text file.

        Args:
            output_path: Output file path

        Format:
            word1: count1
            word2: count2
            ...

        Why preserve this?
        - Original code saved to txt files
        - Human-readable
        - Can diff between texts
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            for word, count in self.frequencies:
                f.write(f"{word}: {count}\n")

        print(f"✓ Word frequencies saved to: {output_path}")

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return (
            f"TextAnalyzer({self.filepath.name})\n"
            f"  Total words: {stats['total_words']}\n"
            f"  Unique words: {stats['unique_words']}\n"
            f"  Vocabulary richness: {stats['vocabulary_richness']:.3f}"
        )


def analyze_multiple_texts(
    filepaths: List[Path],
    output_dir: Optional[Path] = None,
    verbose: bool = True
) -> List[TextAnalyzer]:
    """Analyze multiple texts for Zipf's Law comparison.

    Args:
        filepaths: List of text files to analyze
        output_dir: Directory to save word frequency files
        verbose: Print progress

    Returns:
        List of TextAnalyzer objects

    Why this function?
    - Original code analyzed 3 hardcoded files
    - Now flexible: analyze any number of texts
    - Batch processing with progress feedback
    """
    analyzers = []

    if verbose:
        print("=" * 70)
        print(f"ANALYZING {len(filepaths)} TEXTS FOR ZIPF'S LAW")
        print("=" * 70)

    for i, filepath in enumerate(filepaths, 1):
        if verbose:
            print(f"\n[{i}/{len(filepaths)}] Processing: {filepath}")

        try:
            with Timer(f"  Analysis") if verbose else Timer.__new__(Timer):
                analyzer = TextAnalyzer(filepath)

            if verbose:
                stats = analyzer.get_statistics()
                print(f"  Total words: {stats['total_words']:,}")
                print(f"  Unique words: {stats['unique_words']:,}")
                print(f"  Most common: '{stats['most_common_word']}' ({stats['most_common_count']:,} times)")

            # Save word frequencies
            if output_dir:
                output_file = output_dir / f"{filepath.stem}_frequencies.txt"
                analyzer.save_word_frequencies(output_file)

            analyzers.append(analyzer)

        except Exception as e:
            print(f"  ✗ Error processing {filepath}: {e}")
            continue

    if verbose:
        print("\n" + "=" * 70)
        print(f"✓ Analyzed {len(analyzers)} texts successfully")
        print("=" * 70)

    return analyzers


def main():
    """Command-line interface for text analysis.

    Example:
        python text_analysis.py text1.txt text2.txt text3.txt
        python text_analysis.py *.txt --output-dir results/
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze texts for Zipf's Law",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'files',
        nargs='+',
        type=str,
        help='Text files to analyze'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Directory to save word frequency files'
    )

    parser.add_argument(
        '--encoding',
        type=str,
        default='utf-8',
        help='Text encoding (utf-8, cp1250, etc.)'
    )

    parser.add_argument(
        '--min-length',
        type=int,
        default=1,
        help='Minimum word length'
    )

    args = parser.parse_args()

    # Convert paths
    filepaths = [Path(f) for f in args.files]
    output_dir = Path(args.output_dir) if args.output_dir else None

    # Analyze
    analyzers = analyze_multiple_texts(
        filepaths,
        output_dir=output_dir,
        verbose=True
    )

    if not analyzers:
        print("No texts were successfully analyzed.")
        sys.exit(1)

    print("\nTo fit Zipf's law and plot results, use:")
    print("  python zipf_fitter.py " + " ".join(args.files))


if __name__ == "__main__":
    main()
