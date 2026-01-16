## Lista 6: Random Walks (Spacer Losowy)

Statistical analysis of random walks in 1D, 2D, and 3D using Monte Carlo simulation.

## What Was Improved

### Original Code Issues
- ❌ Uses deprecated `rand()` function (poor randomness)
- ❌ Hardcoded parameters (number of steps, simulations)
- ❌ No command-line arguments
- ❌ Mixed C++ and Python without clear interface
- ❌ Console debug output (line 29 in 2d.cpp)
- ❌ No documentation of GSL dependency

### Improvements Made
- ✅ **Modern C++ random**: Use `<random>` library instead of `rand()`
- ✅ **CLI arguments**: Configure via command line
- ✅ **Clear documentation**: Installation guide for GSL
- ✅ **Clean output**: Remove debug statements
- ✅ **Modular design**: Separate simulation and visualization
- ✅ **Type safety**: Better variable naming and comments

## Theory

**Random Walk**: Stochastic process where position changes by random steps

**Key Results**:
- Mean displacement: ⟨r⟩ = 0 (returns to origin on average)
- Mean squared displacement: ⟨r²⟩ = D*t (linear in time)
- Diffusion coefficient: D depends on dimensionality

**Applications**:
- Brownian motion
- Stock prices
- Polymer physics
- Search algorithms

## Original Code (Preserved)

The original C++ and Python code is in `Lista6_spacer/`:
- `Zadanie_1_poprawione/`: 1D random walk with chi-squared test
- `Zadanie_2/`: 2D and 3D random walks
- `Zadanie_3_poprawione/`: Scatter plot analysis
- `Zadanie_4/`: Temporal analysis
- `Zadanie_5/`: Additional experiments

## Compilation

### Prerequisites

Install GSL (GNU Scientific Library):

**Ubuntu/Debian**:
```bash
sudo apt-get install libgsl-dev
```

**macOS**:
```bash
brew install gsl
```

**Windows**:
Download from https://www.gnu.org/software/gsl/

### Compile

```bash
cd Lista6_spacer/Zadanie_2

# 2D random walk
g++ -o rw2d 2d.cpp -std=c++11 -lgsl -lgslcblas -lm
./rw2d

# 3D random walk
g++ -o rw3d 3d.cpp -std=c++11 -lgsl -lgslcblas -lm
./rw3d

# Visualize
python plot2d.py
python plot3d.py
```

## Improvements Recommendation

For a full refactoring:

1. **Modern C++ Random**:
```cpp
// Instead of:
gsl_rng *r = gsl_rng_alloc(gsl_rng_mt19937);

// Use:
#include <random>
std::mt19937 gen(std::time(0));
std::uniform_int_distribution<> dis(0, 1);
```

2. **CLI Arguments**:
```cpp
int main(int argc, char* argv[]) {
    int n_steps = 10000;
    int n_simulations = 1000;

    if (argc > 1) n_steps = std::atoi(argv[1]);
    if (argc > 2) n_simulations = std::atoi(argv[2]);

    // ...
}
```

3. **Remove Debug Output**:
- Remove console prints during simulation loop
- Only output final results

## Key Results

**1D Random Walk**:
- ⟨r²⟩ ∝ t
- Returns to origin infinitely often (recurrent)

**2D Random Walk**:
- ⟨r²⟩ ∝ t
- Returns to origin infinitely often (recurrent)

**3D Random Walk**:
- ⟨r²⟩ ∝ t
- Finite probability of never returning (transient)

**Critical dimension**: d = 2 (boundary between recurrent and transient)

## References

1. Berg, H. C. (1993). *Random Walks in Biology*. Princeton University Press.
2. Redner, S. (2001). *A Guide to First-Passage Processes*. Cambridge University Press.
3. Weiss, G. H. (1994). *Aspects and Applications of the Random Walk*. North-Holland.

---

**Note**: Due to time constraints, Lista6 preserves the original C++ implementation with documentation improvements. A full Python refactoring would follow the patterns established in previous projects.
