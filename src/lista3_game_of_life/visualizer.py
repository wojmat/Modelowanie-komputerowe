"""Real-time visualization for Conway's Game of Life

Reuses optimized rendering techniques from Lista2_Plamy:
- Dirty rectangle optimization
- Frame rate limiting
- Efficient matplotlib updates
- Keyboard controls

Why almost identical to Lista2 visualizer?
- Cellular automata share same visualization needs
- Code reuse through composition (uses same grid structure)
- Only difference: update rules (handled in simulation.py)
"""

from typing import Optional
import pygame
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from .simulation import GameOfLifeSimulation, GameOfLifeConfig


class GameOfLifeVisualizer:
    """Real-time visualization for Game of Life.

    Why separate class?
    - Visualization independent of simulation logic
    - Can swap rendering backends (pygame → web → terminal)
    - Testable simulation without GUI dependencies
    """

    def __init__(self, simulation: GameOfLifeSimulation, config: Optional[GameOfLifeConfig] = None):
        """Initialize visualizer.

        Args:
            simulation: Simulation instance to visualize
            config: Configuration (uses simulation config if None)
        """
        self.simulation = simulation
        self.config = config or simulation.config

        # Pygame setup
        pygame.init()
        self.screen_width = self.config.screen_width
        self.screen_height = self.config.screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conway's Game of Life")

        # Calculate cell size
        grid_size = self.config.grid_size
        self.cell_width = self.screen_width // grid_size
        self.cell_height = self.screen_height // grid_size

        # Colors
        self.color_dead = (0, 0, 0)  # Black
        self.color_alive = (255, 255, 255)  # White

        # Previous grid for change detection
        self.prev_grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

        # Frame rate control
        self.clock = pygame.time.Clock()
        self.target_fps = 60

        # Matplotlib setup
        self.setup_plots()

        # State
        self.running = True
        self.paused = False

    def setup_plots(self) -> None:
        """Set up matplotlib for live plotting."""
        plt.ion()
        self.fig, (self.ax_density, self.ax_population) = plt.subplots(1, 2, figsize=(12, 4))

        # Density plot
        self.ax_density.set_title('Density Over Time')
        self.ax_density.set_xlabel('Generation')
        self.ax_density.set_ylabel('Density')
        self.ax_density.set_ylim(0, 1)
        self.density_line, = self.ax_density.plot([], [], 'b-')
        self.ax_density.grid(True, alpha=0.3)

        # Population plot
        self.ax_population.set_title('Population Over Time')
        self.ax_population.set_xlabel('Generation')
        self.ax_population.set_ylabel('Live Cells')
        self.population_line, = self.ax_population.plot([], [], 'g-')
        self.ax_population.grid(True, alpha=0.3)

        plt.tight_layout()

    def draw_grid_optimized(self) -> None:
        """Draw only cells that changed (dirty rectangle optimization)."""
        current_grid = self.simulation.grid.current_grid
        grid_size = self.config.grid_size

        # Find changed cells
        changed_mask = (current_grid != self.prev_grid)

        # Only redraw changed cells
        for row in range(grid_size):
            for col in range(grid_size):
                if changed_mask[row, col]:
                    color = self.color_alive if current_grid[row, col] == 1 else self.color_dead

                    pygame.draw.rect(
                        self.screen,
                        color,
                        (col * self.cell_width, row * self.cell_height,
                         self.cell_width, self.cell_height)
                    )

        # Update previous grid
        np.copyto(self.prev_grid, current_grid)

    def update_plots(self) -> None:
        """Update density and population plots efficiently."""
        densities = self.simulation.density_history
        populations = self.simulation.population_history

        if len(densities) > 0:
            generations = list(range(len(densities)))

            # Update density plot
            self.density_line.set_data(generations, densities)
            self.ax_density.set_xlim(0, max(len(densities), 100))

            # Update population plot
            self.population_line.set_data(generations, populations)
            self.ax_population.set_xlim(0, max(len(populations), 100))
            max_pop = max(populations) if populations else 1
            self.ax_population.set_ylim(0, max_pop * 1.1)

            # Redraw
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()

    def handle_events(self) -> None:
        """Handle keyboard and mouse events.

        Controls:
        - SPACE: Pause/Resume
        - R: Reset with new random state
        - S: Save screenshot
        - Q/ESC: Quit
        - C: Clear grid (kill all cells)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    print(f"{'Paused' if self.paused else 'Resumed'} at generation {self.simulation.iteration}")

                elif event.key == pygame.K_r:
                    print("Resetting simulation with new random state...")
                    self.simulation = GameOfLifeSimulation(self.config)
                    self.prev_grid.fill(0)

                elif event.key == pygame.K_c:
                    print("Clearing grid...")
                    self.simulation.grid.current_grid.fill(0)
                    self.prev_grid.fill(0)

                elif event.key == pygame.K_s:
                    self.save_screenshot()

                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.running = False

    def save_screenshot(self) -> None:
        """Save current grid state as image."""
        from common.config import OutputManager
        om = OutputManager(Path("output"), "lista3_game_of_life")

        filename = f"screenshot_gen_{self.simulation.iteration}.png"
        filepath = om.get_plot_path(filename)

        pygame.image.save(self.screen, str(filepath))
        print(f"✓ Screenshot saved: {filepath}")

    def run(self, update_plot_interval: int = 10) -> None:
        """Run interactive visualization.

        Args:
            update_plot_interval: Update plots every N frames
        """
        print("=" * 70)
        print("CONWAY'S GAME OF LIFE - Interactive Visualization")
        print("=" * 70)
        print("Controls:")
        print("  SPACE: Pause/Resume")
        print("  R: Reset with new random state")
        print("  C: Clear grid")
        print("  S: Save screenshot")
        print("  Q/ESC: Quit")
        print("=" * 70)
        print(f"Initial population: {self.simulation.grid.get_population()}")
        print(f"Initial density: {self.simulation.grid.get_density():.4f}")
        print("=" * 70)

        generation = 0

        while self.running:
            # Handle events
            self.handle_events()

            if not self.paused:
                # Update simulation
                self.simulation.update_step()

                # Draw grid
                self.draw_grid_optimized()

                # Update plots periodically
                if generation % update_plot_interval == 0:
                    self.update_plots()

                generation += 1

                # Print stats periodically
                if generation % 100 == 0:
                    pop = self.simulation.grid.get_population()
                    density = self.simulation.grid.get_density()
                    print(f"Generation {generation}: Population = {pop}, Density = {density:.4f}")

                # Check for interesting states
                if self.simulation.detect_extinction():
                    print(f"\n⚠ EXTINCTION at generation {generation}")
                    print("All cells have died. Press R to reset or Q to quit.")
                    self.paused = True

                elif generation > 100 and self.simulation.detect_stable_state():
                    print(f"\n✓ STABLE STATE detected at generation {generation}")
                    print(f"Final population: {self.simulation.grid.get_population()}")
                    print(f"Final density: {self.simulation.grid.get_density():.4f}")
                    self.paused = True

            # Update display
            pygame.display.flip()

            # Limit frame rate
            self.clock.tick(self.target_fps)

        # Cleanup
        pygame.quit()
        plt.ioff()
        plt.show()  # Show final plots

        print(f"\nSimulation ran for {self.simulation.iteration} generations")
        print(f"Final population: {self.simulation.grid.get_population()}")
        print(f"Final density: {self.simulation.grid.get_density():.4f}")


def main():
    """Command-line interface for visualization.

    Example:
        python visualizer.py
        python visualizer.py --size 200 --density 0.3
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Visualize Conway's Game of Life",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--size', type=int, default=100, help='Grid size')
    parser.add_argument('--density', type=float, default=0.3, help='Initial density')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--width', type=int, default=600, help='Window width')
    parser.add_argument('--height', type=int, default=600, help='Window height')

    args = parser.parse_args()

    # Create configuration
    config = GameOfLifeConfig(
        grid_size=args.size,
        initial_density=args.density,
        random_seed=args.seed,
        screen_width=args.width,
        screen_height=args.height
    )

    # Create simulation
    sim = GameOfLifeSimulation(config)

    # Create and run visualizer
    viz = GameOfLifeVisualizer(sim, config)
    viz.run()


if __name__ == "__main__":
    main()
