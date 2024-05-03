#include <iostream>
#include <fstream>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <cmath>
#include <iomanip>

int main() {
    const gsl_rng_type * T;
    gsl_rng * r;

    int n = 1000; // number of steps
    double x = 0, y = 0; // start at the origin, using double for better precision

    std::ofstream file;
    file.open("random_walk_2D.txt");

    gsl_rng_env_setup();

    T = gsl_rng_default;
    r = gsl_rng_alloc(T);

    gsl_rng_set(r, time(NULL)); // Set the seed based on current time for randomness

    file << "0,0" << std::endl;  // Save the starting point

    for (int i = 0; i < n; i++) {
        double angle = gsl_ran_flat(r, 0, 2 * M_PI);
        std::cout << "Step " << i << ": Angle = " << angle << std::endl; // Debug output to console
        x += cos(angle);
        y += sin(angle);
        file << std::fixed << std::setprecision(4) << x << "," << y << std::endl;  // Ensure precision for small increments
    }

    file.close();
    gsl_rng_free(r);
    return 0;
}
