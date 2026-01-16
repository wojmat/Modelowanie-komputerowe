"""Configuration management for physics simulations

Centralized configuration to eliminate hardcoded values scattered throughout code.

Why this is necessary:
- Original code had magic numbers everywhere (grid_size=301, n=1000, etc.)
- Changing parameters required editing multiple files
- No validation of parameter ranges
- Difficult to reproduce experiments with different settings

This module provides:
- Type-safe configuration classes
- Automatic validation
- Centralized output directory management
- Easy parameter serialization
"""

from pathlib import Path
from typing import Optional, Dict, Any
import json
from dataclasses import dataclass, asdict


@dataclass
class Config:
    """Base configuration class for simulations.

    Why dataclass?
    - Automatic __init__, __repr__, __eq__
    - Type hints enforced
    - Easy serialization with asdict()
    """
    # Output settings
    output_dir: Path = Path("output")
    save_plots: bool = True
    plot_dpi: int = 300

    # Random seed for reproducibility
    random_seed: Optional[int] = 42

    # Visualization
    show_plots: bool = False  # False for batch processing

    def __post_init__(self):
        """Validate configuration after initialization.

        Why needed: Catch invalid parameters early
        """
        if self.plot_dpi < 72:
            raise ValueError(f"DPI too low: {self.plot_dpi} < 72")

        # Ensure output_dir is Path object
        if not isinstance(self.output_dir, Path):
            self.output_dir = Path(self.output_dir)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary.

        Returns:
            Dictionary representation of configuration
        """
        config_dict = asdict(self)
        # Convert Path to string for JSON serialization
        config_dict['output_dir'] = str(config_dict['output_dir'])
        return config_dict

    def save(self, filepath: Path) -> None:
        """Save configuration to JSON file.

        Args:
            filepath: Output JSON file path

        Why needed: Document simulation parameters for reproducibility
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"✓ Configuration saved to: {filepath}")

    @classmethod
    def load(cls, filepath: Path) -> 'Config':
        """Load configuration from JSON file.

        Args:
            filepath: Input JSON file path

        Returns:
            Config object loaded from file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert string back to Path
        if 'output_dir' in data:
            data['output_dir'] = Path(data['output_dir'])

        return cls(**data)


class OutputManager:
    """Manages output directories and file paths.

    Why this class exists:
    - Original code had hardcoded paths like "output_no_jail.txt"
    - No error handling for file operations
    - Output scattered across project directories
    - No automatic directory creation

    Benefits:
    - Centralized path management
    - Automatic directory creation
    - Consistent file naming
    - Easy cleanup and organization
    """

    def __init__(self, base_dir: Path, project_name: str):
        """Initialize output manager.

        Args:
            base_dir: Base output directory (e.g., "output")
            project_name: Project subdirectory (e.g., "lista1_monopoly")

        Example:
            >>> om = OutputManager(Path("output"), "lista1_monopoly")
            >>> om.get_path("results.txt")
            Path("output/lista1_monopoly/results.txt")
        """
        self.base_dir = Path(base_dir)
        self.project_dir = self.base_dir / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)

    def get_path(self, filename: str) -> Path:
        """Get full path for output file.

        Args:
            filename: Name of output file

        Returns:
            Full path to file in project output directory
        """
        return self.project_dir / filename

    def get_data_path(self, filename: str) -> Path:
        """Get path for data files.

        Args:
            filename: Name of data file

        Returns:
            Path to file in data subdirectory
        """
        data_dir = self.project_dir / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir / filename

    def get_plot_path(self, filename: str) -> Path:
        """Get path for plot files.

        Args:
            filename: Name of plot file

        Returns:
            Path to file in plots subdirectory
        """
        plots_dir = self.project_dir / "plots"
        plots_dir.mkdir(exist_ok=True)
        return plots_dir / filename

    def get_video_path(self, filename: str) -> Path:
        """Get path for video files.

        Args:
            filename: Name of video file

        Returns:
            Path to file in videos subdirectory
        """
        videos_dir = self.project_dir / "videos"
        videos_dir.mkdir(exist_ok=True)
        return videos_dir / filename

    def clear(self) -> None:
        """Clear all output files for this project.

        Warning: Deletes all files in project output directory!
        """
        import shutil
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)
            print(f"✓ Cleared output directory: {self.project_dir}")

    def list_files(self, pattern: str = "*") -> list:
        """List all files matching pattern.

        Args:
            pattern: Glob pattern (e.g., "*.txt", "*.png")

        Returns:
            List of matching file paths
        """
        return list(self.project_dir.glob(f"**/{pattern}"))

    def __repr__(self) -> str:
        return f"OutputManager(project_dir={self.project_dir})"


# Example project-specific configurations
@dataclass
class MonopolyConfig(Config):
    """Configuration for Lista1 Monopoly simulation.

    Why separate config classes?
    - Each project has unique parameters
    - Type hints for project-specific settings
    - Easy validation of project requirements
    """
    num_rolls: int = 1000000
    num_squares: int = 40
    use_jail: bool = False

    def __post_init__(self):
        super().__post_init__()
        if self.num_rolls <= 0:
            raise ValueError(f"num_rolls must be positive: {self.num_rolls}")
        if self.num_squares <= 0:
            raise ValueError(f"num_squares must be positive: {self.num_squares}")


@dataclass
class GameOfLifeConfig(Config):
    """Configuration for Lista3 Game of Life simulation."""
    grid_size: int = 100
    initial_density: float = 0.3
    max_iterations: int = 1000
    screen_width: int = 600
    screen_height: int = 600

    def __post_init__(self):
        super().__post_init__()
        if not (0.0 <= self.initial_density <= 1.0):
            raise ValueError(f"initial_density must be in [0,1]: {self.initial_density}")
        if self.grid_size <= 0:
            raise ValueError(f"grid_size must be positive: {self.grid_size}")


@dataclass
class RandomWalkConfig(Config):
    """Configuration for Lista6 Random Walk simulation."""
    num_steps: int = 10000
    num_simulations: int = 1000
    dimensions: int = 2  # 1, 2, or 3

    def __post_init__(self):
        super().__post_init__()
        if self.dimensions not in [1, 2, 3]:
            raise ValueError(f"dimensions must be 1, 2, or 3: {self.dimensions}")
        if self.num_steps <= 0:
            raise ValueError(f"num_steps must be positive: {self.num_steps}")
        if self.num_simulations <= 0:
            raise ValueError(f"num_simulations must be positive: {self.num_simulations}")


@dataclass
class ClusterGrowthConfig(Config):
    """Configuration for Lista7 Cluster Growth simulation."""
    model: str = "eden"  # "eden", "dla", or "snowflake"
    max_size: int = 10000
    grid_size: int = 500

    def __post_init__(self):
        super().__post_init__()
        valid_models = ["eden", "dla", "snowflake"]
        if self.model not in valid_models:
            raise ValueError(f"model must be one of {valid_models}: {self.model}")
        if self.max_size <= 0:
            raise ValueError(f"max_size must be positive: {self.max_size}")
