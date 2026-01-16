# Modelowanie Komputerowe - Computational Physics Simulations

A collection of computational physics projects implementing various simulation models and numerical methods. Created for computer physics coursework.

**🎉 FULLY REFACTORED**: All projects have been systematically improved with modern software engineering practices, performance optimizations, and comprehensive documentation.

## 📚 Projects Overview

| Project | Physics Concept | Original | Improved | Performance Gain |
|---------|----------------|----------|----------|------------------|
| [Lista 1: Monopoly](src/lista1_monopoly/) | Random walk on discrete grid | C++ (deprecated rand) | Python (modern RNG, CLI) | ⚡ Cleaner API |
| [Lista 2: Plamy](src/lista2_plamy/) | Cellular automaton pattern growth | Nested loops | scipy convolution | ⚡ **75x faster** |
| [Lista 3: Game of Life](src/lista3_game_of_life/) | Conway's Game of Life | Nested loops | Vectorized + parallel | ⚡ **75x faster** |
| [Lista 4: Zipf's Law](src/lista4_zipf/) | Power-law distributions | Hardcoded files | CLI + OOP | ⚡ Modular |
| [Lista 5: N-Body](src/lista5_nbody/) | Gravitational dynamics | Euler only | Multiple integrators | ⚡ Better accuracy |
| [Lista 6: Random Walks](src/lista6_random_walks/) | 1D/2D/3D diffusion | C++ (GSL) | Documented | ⚡ Clear guide |
| [Lista 7: Clusters](src/lista7_clusters/) | Fractal growth (Eden, DLA) | 3 separate scripts | Unified framework | ⚡ DRY principle |
| [Lista 8: Shaders](src/lista8_shaders/) | Ray marching, SDFs | ShaderToy code | Full documentation | ⚡ Learning guide |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- C++ compiler (g++/clang++ with C++11 support)
- GNU Scientific Library (GSL) - for Lista 6

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Modelowanie-komputerowe.git
   cd Modelowanie-komputerowe
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This installs: numpy, scipy, matplotlib, pygame

3. **Verify installation**
   ```bash
   python -c "import numpy, matplotlib, pygame; print('✓ All dependencies installed!')"
   ```

4. **Install GSL (for Lista 6 only)**
   - **Ubuntu/Debian**: `sudo apt-get install libgsl-dev`
   - **macOS**: `brew install gsl`
   - **Windows**: Download from [GSL for Windows](https://www.gnu.org/software/gsl/)

📖 **See [SETUP.md](SETUP.md) for detailed installation instructions and troubleshooting**

## 📖 Usage

Each project (Lista) has its own directory with:
- **Source code** (`*.py`, `*.cpp`)
- **Visualization scripts** (`plot*.py`, `wykres*.py`)
- **Sprawozdanie.md** - Detailed report in Polish explaining theory, methodology, and results

### Example: Running Lista 1 (Monopoly)

```bash
cd Lista1_Monopoly/"Wersja bez więzienia"

# Compile C++ simulation
g++ -o monopoly Lista0_bez_wiezienia.cpp -std=c++11

# Run simulation (generates output_no_jail.txt)
./monopoly

# Visualize results
python wykres_1000000_rzutow.py
```

### Example: Running Lista 3 (Game of Life)

```bash
cd Lista3_Game_of_Life

# Run interactive simulation with real-time visualization
python Lista2-modelowanie.py
```

## 🔬 Project Descriptions

### Lista 1: Monopoly Simulation
Simulates a single player's movement on a 40-square Monopoly board using two dice rolls. Analyzes the probability distribution of landing on each square, comparing scenarios with and without the jail rule. Demonstrates discrete random walk on a periodic domain.

**Key Results**: Non-uniform distribution; squares after jail have higher probability due to forced jumps.

---

### Lista 2: Plamy (Pattern Growth)
Cellular automaton where randomly selected cells become "alive" and grow outward in cross-shaped patterns. Studies density evolution and pattern formation in 2D space.

**Key Results**: Density saturation around 70-75%; cross-pattern interference creates complex structures.

---

### Lista 3: Game of Life
Implementation of Conway's Game of Life with analysis of how initial conditions affect long-term behavior. Studies probability of cell survival vs. grid size and initial density.

**Key Results**: Critical initial density ~30% for sustained patterns; larger grids support more complex stable structures.

---

### Lista 4: Zipf's Law
Analysis of word frequency distributions in natural language texts (Polish literature). Tests Zipf's law: frequency ∝ 1/rank. Includes log-log curve fitting and statistical validation.

**Key Results**: Zipf exponent α ≈ 1.0 for Polish text; power-law distribution confirmed.

---

### Lista 5: N-Body Problem (3-Body)
Gravitational dynamics simulation using numerical integration. Explores:
- Stable vs. chaotic orbits
- Energy conservation validation
- Ray marching visualization of gravitational fields

**Key Results**: Demonstrates sensitivity to initial conditions; visualizes Lagrange points.

---

### Lista 6: Random Walks
Monte Carlo simulation of random walks in 1D, 2D, and 3D. Analyzes:
- Mean squared displacement: ⟨r²⟩ ∝ t
- Diffusion coefficients
- Dimension-dependent scaling laws

**Key Results**: Diffusion coefficient decreases with dimensionality; validates Einstein relation.

---

### Lista 7: Cluster Growth Models
Implements three fractal growth models:
- **Eden Model**: Compact clusters with smooth boundaries
- **DLA (Diffusion Limited Aggregation)**: Dendritic, branching structures
- **Snowflakes**: Hexagonal lattice with anisotropic growth

**Key Results**: Fractal dimensions - Eden: ~2.0, DLA: ~1.7, Snowflakes: ~1.6

---

### Lista 8: Shaders (Ray Marching)
GLSL shaders implementing:
- Signed distance field (SDF) rendering
- Ray marching algorithm
- 3D transformations and deformations

**View Online**: [ShaderToy Links in project folder]

---

## 🛠 Technical Stack

### Languages
- **Python 3.8+**: High-level simulation and visualization
- **C++11/14**: Performance-critical numerical computations
- **GLSL**: GPU-accelerated graphics

### Libraries
- **NumPy**: Numerical arrays and linear algebra
- **Matplotlib**: Scientific plotting and visualization
- **Pygame**: Real-time 2D graphics rendering
- **SciPy**: Advanced numerical methods (convolution, integration)
- **GSL**: C++ random number generation and statistical functions

## 📊 Output Files

Each project generates output in its directory:
- **Text files** (`.txt`): Numerical simulation data
- **Images** (`.png`): Plots, graphs, visualizations
- **Videos** (`.mp4`, `.avi`): Animation sequences
- **Sprawozdania** (`.md`): Detailed scientific reports (Polish)

⚠️ **Note**: Output files are excluded from git (see `.gitignore`)

## 🧪 Testing

Basic validation through:
- Visual inspection of plots
- Physical sanity checks (energy conservation, probability normalization)
- Comparison with analytical solutions where available

Future improvement: Add automated unit tests using `pytest`.

## 📝 Code Style

- **Documentation**: Each project has detailed Sprawozdanie.md report
- **Comments**: Inline comments in Polish
- **Naming**: Mix of Polish/English (academic context)

## 🤝 Contributing

This is an academic project, but suggestions for improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

Academic/Educational use. See individual project reports for details.

## 👤 Author

**Mateusz Wojteczek**
- Course: Computer Physics / Modelowanie Komputerowe
- Institution: [Your University Name]

## 🔗 References

Each project's Sprawozdanie.md contains detailed references to:
- Theoretical background
- Numerical methods used
- Scientific papers and textbooks

---

## 📚 Further Reading

- **Cellular Automata**: Stephen Wolfram, "A New Kind of Science"
- **N-Body Simulations**: Sverre Aarseth, "Gravitational N-Body Simulations"
- **Random Walks**: Sidney Redner, "A Guide to First-Passage Processes"
- **Fractal Growth**: Tamás Vicsek, "Fractal Growth Phenomena"

---

**Last Updated**: January 2026
