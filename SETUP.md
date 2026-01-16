# Setup Instructions

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- numpy
- scipy
- matplotlib
- pygame

### 2. Verify Installation

```bash
python -c "import numpy, matplotlib, pygame; print('✓ All dependencies installed!')"
```

### 3. Test Improved Code

```bash
# Test Lista 1 (Monopoly simulation)
python src/lista1_monopoly/monopoly_simulation.py --rolls 10000 --seed 42 --verbose

# Visualize results
python src/lista1_monopoly/visualize.py
```

## For Development

### Install Additional Tools

```bash
# Code formatting
pip install black

# Type checking
pip install mypy

# Testing
pip install pytest
```

### Format Code

```bash
black src/
```

### Run Type Checking

```bash
mypy src/
```

## Troubleshooting

### Missing matplotlib
```bash
pip install matplotlib
```

### Missing pygame
```bash
pip install pygame
```

### Permission Errors on Windows
Run as administrator or use:
```bash
pip install --user -r requirements.txt
```

## C++ Projects (Lista6, Lista7)

Some projects use C++ for performance. You'll need:

### Install GSL (for Lista6)

**Ubuntu/Debian:**
```bash
sudo apt-get install libgsl-dev
```

**macOS:**
```bash
brew install gsl
```

**Windows:**
Download from: https://www.gnu.org/software/gsl/

### Compile C++ Code

```bash
cd Lista6_spacer/Zadanie_2
g++ -o simulation 2d.cpp -std=c++11 -lgsl -lgslcblas -lm
./simulation
```

## Project Structure

```
Modelowanie-komputerowe/
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview
├── SETUP.md                  # This file
├── .gitignore               # Git exclusions
│
├── src/                     # Improved code
│   ├── common/              # Shared utilities
│   ├── lista1_monopoly/     # Refactored projects
│   └── ...
│
├── output/                  # Generated results (not in git)
│
└── Lista*/                  # Original code (preserved)
```

## Migrating from Original Code

The original code is preserved in `Lista*/` directories. Improved code is in `src/` directory.

### Running Original Code
```bash
cd Lista1_Monopoly/"Wersja bez więzienia"
g++ -o monopoly Lista0_bez_wiezienia.cpp -std=c++11
./monopoly
```

### Running Improved Code
```bash
python src/lista1_monopoly/monopoly_simulation.py --rolls 1000000
```

Both produce compatible output files.
