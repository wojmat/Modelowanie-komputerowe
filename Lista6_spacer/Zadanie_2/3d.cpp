#include <iostream>
#include <fstream>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <cmath>

int main() {
    const gsl_rng_type * T;
    gsl_rng * r;

    int n = 1000; // number of steps
    int x = 0, y = 0, z = 0; // start at the origin

    std::ofstream file;
    file.open("random_walk_3D.txt");

    gsl_rng_env_setup();

    T = gsl_rng_default;
    r = gsl_rng_alloc(T);

    file << "0,0,0" << std::endl; // Save the starting point

    for (int i = 0; i < n; i++) {
        double phi = gsl_ran_flat(r, 0, 2 * M_PI);
        double theta = acos(gsl_ran_flat(r, -1, 1));
        x += sin(theta) * cos(phi);
        y += sin(theta) * sin(phi);
        z += cos(theta);
        file << x << "," << y << "," << z << std::endl;
    }

    file.close();
    gsl_rng_free(r);
    return 0;
}
